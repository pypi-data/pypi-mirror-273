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
# pylint: disable=multiple-statements


import re
import json
from typing import List, Optional
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import BuildError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page


from ...__version__ import __version__
from ..tools_and_constants import ICONS_IN_TEMPLATES_DIR
from ..deprecation import deprecation_warning
from ..messages import Lang
from ..pyodide_logger import logger
from .maestro_tools import ConfigExtractor, dump_and_dumper
from .config import PyodideMacrosConfig






NO_DUMP = tuple('''
    docs_dir_path
    docs_dir_cwd_rel
    lang
    page
'''.split())





class BaseMaestro( BasePlugin[PyodideMacrosConfig] ):
    """
    Main class, regrouping the basic configurations, properties, getters and/or constants
    for the different children classes: each of them will inherit from MaestroConfig.
    It is also used as "sink" for the super calls of other classes that are not implemented
    on the MacrosPlugin class.

    Note that, for the ConfigExtractor for to properly work, the class hierarchy has to
    extend MacrosPlugin at some point.
    """

    ignore_macros_plugin_diffs:              bool = ConfigExtractor('build')
    skip_py_md_paths_names_validation:       bool = ConfigExtractor('build')
    load_yaml_encoding:                      str  = ConfigExtractor('build')
    macros_with_indents:                List[str] = ConfigExtractor('build')
    encrypt_corrections_and_rems:            bool = ConfigExtractor('build')
    forbid_secrets_without_corr_or_REMs:     bool = ConfigExtractor('build')
    forbid_hidden_corr_and_REMs_without_secrets: bool = ConfigExtractor('build')
    forbid_corr_and_REMs_with_infinite_attempts: bool = ConfigExtractor('build')
    python_libs:                        List[str] = ConfigExtractor('build')
    # bypass_indent_errors:                  bool = ConfigExtractor('build')
    # check_python_files:                    bool = ConfigExtractor('build')
    # soft_check:                            bool = ConfigExtractor('build')

    show_assertion_code_on_failed_test:      bool = ConfigExtractor("ides")
    max_attempts_before_corr_available:      bool = ConfigExtractor("ides")
    decrease_attempts_on_user_code_failure:  bool = ConfigExtractor("ides")
    default_ide_height_lines:                 int = ConfigExtractor("ides")
    deactivate_stdout_for_secrets: Optional[bool] = ConfigExtractor("ides")
    show_only_assertion_errors_for_secrets: Optional[bool] = ConfigExtractor("ides")

    default_height_ide_term:              int = ConfigExtractor("terms")
    default_height_isolated_term:             int = ConfigExtractor("terms")
    stdout_cut_off:                           int = ConfigExtractor("terms")


    hide:    Optional[bool] = ConfigExtractor("qcms")
    multi:   Optional[bool] = ConfigExtractor("qcms")
    shuffle: Optional[bool] = ConfigExtractor("qcms")

    _dev_mode:               bool = ConfigExtractor()
    j2_block_start_string:    str = ConfigExtractor()
    j2_block_end_string:      str = ConfigExtractor()
    j2_variable_start_string: str = ConfigExtractor()
    j2_variable_end_string:   str = ConfigExtractor()

    scripts_url: str = ConfigExtractor("_others")
    site_root:   str = ConfigExtractor("_others")


    # global mkdocs config data:
    docs_dir:    str = ConfigExtractor(root='_conf')
    repo_url:    str = ConfigExtractor(root='_conf')
    site_name:   str = ConfigExtractor(root='_conf')
    site_url:    str = ConfigExtractor(root='_conf')
    site_dir:    str = ConfigExtractor(root='_conf')


    #----------------------------------------------------------------------------
    # WARNING: the following properties are assigned from "other places":
    #   - pages from the original MacrosPlugin
    #   - others from PyodideMacrosPlugin

    page: Page  # just as a reminder: defined by MacrosPlugin

    docs_dir_path: Path
    """ Current docs_dir of the project as a Path object (ABSOLUTE path) """

    docs_dir_cwd_rel: Path
    """ docs_dir Path object, but relative to the CWD, at runtime """

    _macro_with_indent_pattern:re.Pattern = None
    """
    Pattern to re.match macro calls that will need to handle indentation levels.
    Built at runtime (depends on `macro_with_indents`)
    """


    #----------------------------------------------------------------------------

    button_icons_directory:str = ""
    base_url:str = ""
    pmt_url:str = 'https://gitlab.com/frederic-zinelli/pyodide-mkdocs-theme'
    version:str = __version__

    lang: Lang = None


    def on_config(self, config:MkDocsConfig):       # pylint: disable=missing-function-docstring

        self.lang = Lang()
        self.lang.register_env(self)

        if self.skip_py_md_paths_names_validation:
            logger.warning("skip_py_md_paths_names_validation option is activated.")

        super().on_config(config)   # pylint: disable-next=no-member
                                    # MacrosPlugin is actually "next in line" and has the method


    #----------------------------------------------------------------------------

    def location(self, page:Optional[Page]=None):
        """ Path to the current file, relative to the cwd. """
        page = page or getattr(self, 'page', None)
        if not page:
            raise BuildError("No page defined yet")
        return f"{ self.docs_dir_cwd_rel }/{ page.file.src_uri }"


    def level_up_from_current_page(self, url:str=None) -> str:
        """
        Return the appropriate number of ".." steps needed to build a relative url to go from the
        current page url back to the root directory.

        Note there are no trailing backslash.

        @url: relative to the docs_dir (ex: "exercices/ ..."). If None, use self.page.url instead.
        """
        url = self.page.url if url is None else url
        page_loc:Path = self.docs_dir_path / url
        segments = page_loc.relative_to(self.docs_dir_path).parts
        out = len(segments) * ['..']
        return '/'.join(out) or '.'


    #----------------------------------------------------------------------------


    def rebase(self, base_url:str):
        """
        Necessary for development only (to replace the wrong base_url value during a serve in the
        theme project)
        NOTE: Keep in mind the base_url SOMETIMES ends with a slash...
        """
        return base_url if base_url!='/' else '.'


    def dump_to_js_config(self, base_url):
        """
        Create the <script> tag that will add all the CONFIG properties needed in the JS
        global config file, and also applies the post conversion where needed.
        """

        to_dump = [
            p for p in sorted(BaseMaestro.__annotations__)
              if not p.startswith('_') and p not in NO_DUMP
                 or p=='_dev_mode' and self and self._dev_mode
        ]

        if self:                                # HACK!
            # pylint: disable=w0201
            base_url = self.rebase(base_url).rstrip('/')
            self.button_icons_directory = f"{base_url}/{ICONS_IN_TEMPLATES_DIR}"
            self.base_url = base_url

        dct = dump_and_dumper(to_dump, self, json.dumps)
        dct['lang'] = Lang.dump_as_str(self and self.lang)

        if self is None:                        # HACK!
            # Dump to config.js (helper):
            dumping = [ f"\n    { prop }: { val }," for prop,val in dct.items() ]
            return ''.join(dumping)

        # Dump to main.html...
        dumping = [ f"\n  CONFIG.{ prop } = { val }" for prop,val in dct.items() ]

        # ... adding post conversions operations.
        out = f'''\
<script type="application/javascript">
{ "".join(dumping) }
CONFIG.lang.tests.as_pattern = new RegExp(CONFIG.lang.tests.as_pattern, 'i')
CONFIG.pythonLibs = new Set(CONFIG.pythonLibs)
</script>'''
        return out


    #----------------------------------------------------------------------------


    def _omg_they_killed_keanu(self,page_name:str, page_on_context:Page=None):
        """ Debugging purpose only. Use as breakpoint utility.
            @page_on_context argument used when called "outside" of the macro logic (fro example,
            in external hooks)
        """
        page = page_on_context or self.page
        if page_name == page.url:
            logger.error("Breakpoint! (the CALL to this method should be removed)")


    def warn_unmaintained(self, that:str):
        """
        Generic warning message for people trying to used untested/unmaintained macros.
        """
        deprecation_warning(
            f"{ that.capitalize() } has not been maintained since the original pyodide-mkdocs "
            "project, may not currently work, and will be removed in the future.\n"
            "Please open an issue on the pyodide-mkdocs-theme repository, if you need it.\n\n"
            f"\t{ self.pmt_url }"
        )
