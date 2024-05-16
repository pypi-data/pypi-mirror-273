"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""


import os
import re
import shutil
from collections import defaultdict
from functools import wraps
from pathlib import Path

from mkdocs.structure.files import Files, File
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import BuildError
from mkdocs_macros.plugin import MacrosPlugin





from ...__version__ import __version__
from ..exceptions import PyodideConfigurationError
from ..tools_and_constants import PY_LIBS
from ..pyodide_logger import logger
from ..macros import (
    autres,
    IDEs,
    isolated_components,
    qcm,
)
from .config import MISSING_MACROS_PROPS, EXTRAS_MACROS_PROPS
from .maestro_base import BaseMaestro
from .maestro_indent import MaestroIndent
from .maestro_IDE import MaestroIDE
from .maestro_extras import MaestroExtras







class PyodideMacrosPlugin(
    MaestroExtras,
    MaestroIDE,
    MaestroIndent,
    BaseMaestro,
    MacrosPlugin,    # Always last, so that other classes may trigger super methods appropriately.
):
    """
    Class centralizing all the behaviors of the different parent classes.

    This is kinda the "controller", linking all the behaviors to mkdocs machinery, while the
    parent classes hold the "somewhat self contained" behaviors.

    For reference, here are the hooks defined in the original MacrosPlugin:
        - on_config
        - on_nav
        - on_page_markdown  (+ on_pre_page_macros + on_post_page_macros)
        - on_post_build     (on_post_build macros)
        - on_serve
    """


    # Override
    def on_config(self, config:MkDocsConfig):
        # pylint: disable=attribute-defined-outside-init
        # --------------------------------------------------------------
        # Section to always apply first:

        self._conf = config # done in MacrosPlugin, but also done here because needed here or there

        self.docs_dir_path    = Path(config.docs_dir)
        self.docs_dir_cwd_rel = self.docs_dir_path.relative_to(Path.cwd())

        # --------------------------------------------------------------

        self._check_macros_plugin_props()
        self._check_docs_paths_validity()

        super().on_config(config)



    def on_files(self, files: Files, /, *, config: MkDocsConfig):
        """
        If python libs directories are registered, create one archive for each of them.
        It's on the responsibility of the user to work with them correctly...
        """
        for py_str in self.python_libs:
            py_path = Path(py_str)

            if py_str.endswith('.py'):
                raise BuildError(
                    f"Python libraries must be packages but was: {py_str}.\n\n"
                    "(package = a directory with at least an __init__.py file, "
                    "and possibly other files or packages)"
                )
            elif not py_path.exists():
                if py_str != PY_LIBS:
                    logger.warning(f"Invalid python library: {py_str} not found")
                continue
            if len(py_path.parts) > 1:
                raise BuildError(
                    f"Python libraries have to be directly in the CWD, but was: {py_str}"
                )

            # Remove any cached files to make the archive lighter (the version won't match
            # pyodide compiler anyway!):
            for cached in py_path.rglob("*.pyc"):
                cached.unlink()

            shutil.make_archive(py_path, 'zip', py_path)
            files.append(
                File(py_str+'.zip', '.', Path(self.site_dir), False)
            )


    # Override
    def on_post_build(self, config: MkDocsConfig) -> None:
        """
        Suppress the python archives from the CWD.
        """
        for py_str in self.python_libs:
            file = Path(py_str+'.zip')
            file.unlink(missing_ok=True)

        super().on_post_build(config)


    #--------------------------------------------------------------------------



    # Override
    def _load_modules(self):
        """ Override the super method to register the Pyodide macros at appropriate time """

        def macro_with_warning(func):
            macro = func(self)
            logged = False          # log once only only per macro...

            @wraps(func)
            def wrapper(*a,**kw):
                nonlocal logged
                if not logged:
                    logged = True
                    self.warn_unmaintained(f'The macro {func.__name__!r}')
                return macro(*a,**kw)
            return wrapper


        macros = [
            IDEs.IDE,
            IDEs.IDEv,
            IDEs.terminal,
            IDEs.py_btn,
            IDEs.section,

            qcm.multi_qcm,

            # isolated_components.py_sujet,     # just an alias for py, actually...
            isolated_components.py,
        ]
        old_macros = [
            autres.cours,
            autres.exercice,
            autres.ext,
            autres.html_fig,
            autres.numworks,
            autres.python_carnet,
            autres.python_ide,
            autres.tit,
            autres.mult_col,
        ]

        for func in macros:
            self.macro(func(self))

        for func in old_macros:
            self.macro( macro_with_warning(func) )

        super()._load_modules()



    # Override
    def _load_yaml(self):
        """
        Override the MacrosPlugin method, replacing on the fly `__builtins__.open` with a version
        handling the encoding.
        """
        # pylint: disable=multiple-statements
        src_open = open
        def open_with_utf8(*a,**kw):
            return src_open(*a,**kw, encoding=self.load_yaml_encoding)

        # Depending on the python version/context, the __builtins__ can be of different types
        as_dct = isinstance(__builtins__, dict)

        if as_dct:  __builtins__['open'] = open_with_utf8
        else:       __builtins__.open = open_with_utf8
        try:
            super()._load_yaml()
        finally:
            if as_dct:  __builtins__['open'] = src_open
            else:       __builtins__.open = src_open



    #--------------------------------------------------------------------------



    def _check_docs_paths_validity(self) -> None :
        """
        Travel through all paths in the docs_dir and raises an BuildError if "special characters"
        are found in directory, py, or md file names (accepted characters are: r'[\\w.-]+' )
        """
        if self.skip_py_md_paths_names_validation:
            return

        invalid_chars = re.compile(r'[^A-Za-z0-9_.-]+')
        wrongs = defaultdict(list)

        # Validation is done on the individual/current segments of the paths, so that an invalid
        # directory name is not affecting the validation of its children.
        for path,dirs,files in os.walk(self.docs_dir):
            files_to_check = [ file for file in files if re.search(r'\.(py|md)$', file)]
            for segment in dirs + files_to_check:
                invalids = frozenset(invalid_chars.findall(segment))
                if invalids:
                    wrongs[invalids].append( os.path.join(path,segment) )

        if wrongs:
            msg = ''.join(
                f"\nWrong characters { repr(''.join(sorted(invalids))) } in:"
                + "".join(f"\n\t{ path }" for path in sorted(lst))
                for invalids,lst in wrongs.items()
            )
            raise BuildError(f'Found path(s) with invalid characters:{ msg }')



    def _check_macros_plugin_props(self):
        """ Verify that the config of the MacroPlugin class is still the expected one """

        if not MISSING_MACROS_PROPS and not EXTRAS_MACROS_PROPS:
            return

        if self.ignore_macros_plugin_diffs:
            logger.error(
                "Inconsistent MacrosPlugin properties / ignore_macros_plugin_diffs is set to true"
            )

        else:
            raise PyodideConfigurationError(f"""
Cannot configure PyodideMacrosPlugin: the basic configuration of MacrosPlugin changed:
{MISSING_MACROS_PROPS}{EXTRAS_MACROS_PROPS}"""
"\nIf you absolutely need to run mkdocs before any fix is done, you can try the option "
"`ignore_macros_plugin_diffs: true` in the `plugin_macros` section of `mkdocs.yml`, "
"but there are no guarantees the build will succeed, depending on what the changes were.\n\n")
