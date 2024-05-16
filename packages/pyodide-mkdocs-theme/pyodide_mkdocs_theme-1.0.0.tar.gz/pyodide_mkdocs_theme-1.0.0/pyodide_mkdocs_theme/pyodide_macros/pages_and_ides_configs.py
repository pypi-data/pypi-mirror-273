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


import json
from typing import Any, Dict, List, Set, Tuple, Type, TYPE_CHECKING
from itertools import starmap
from dataclasses import dataclass
from math import inf



from .tools_and_constants import KIND_ORDER, EditorName, ScriptKind
from .pyodide_logger import logger
from .parsing import compress_LZW
from . import html_builder as Html

if TYPE_CHECKING:
    from .plugin.pyodide_macros_plugin import PyodideMacrosPlugin




MAYBE_LISTS: Tuple[str,...] = ('excluded', 'excluded_methods', 'white_list')


@dataclass
class IdeConfig:
    """
    Configuration of one IDE in one page of the documentation. Convertible to JS, to define the
    global variable specific to each page.

    Always instantiated without arguments, and items are updated when needed.
    """

    py_name:      str = ""          # name to use for downloaded file
    env_content:  str = ""          # HDR part of "exo.py"
    user_content: str = ""          # Non-HDR part of "exo.py" (initial code)
    #corr_content: str = ""         # not exported to JS!
    public_tests: str = ""          # test part of "exo.py" (initial code)
    secret_tests: str = ""          # Content of "exo_test.py" (private tests)
    post_content: str = ""          # Content to run after executions are done

    excluded: List[str] = None      # List of forbidden instructions (functions or packages)
    excluded_methods: List[str] = None # List of forbidden methods accesses
    rec_limit: int = None           # recursion depth to use at runtime, if defined (-1 otherwise).
    white_list: List[str] = None    # White list of packages to preload at runtime

    attempts_left: int = None       # Not overwriting this means there is no counter displayed
    auto_log_assert: bool = None    # If None, use the global setting, CONFIG.showAssertionCodeOnFailedTest
    corr_rems_mask: int = None      # Bit mask:   has_corr=corr_rems_mask&1 ; has_rem=corr_rems_mask&2
    has_check_btn: bool = None      # Store the info about the Ide having its check button visible or not

    prefill_term: str = None        # Command to insert in the terminal after it's startup.



    def dump_to_js_code(self):
        """
        Convert the current config to a valid string representation of a JS object.
        """
        content = ', '.join(
            f'"{k}": { typ }'                  # pylint: disable-next=no-member
            for k,typ in starmap(self._convert, self.__class__.__annotations__.items())
            if typ is not None      # This filtering operation
        )
        return f"{ '{' }{ content }{ '}' }"


    def _convert(self, prop:str, typ:Type):
        """
        Convert the current python value to the equivalent "code representation" for a JS file.
        @prop: property name to convert
        @typ: type (annotation) of the property
        @returns: str
        """
        val = getattr(self, prop)
        if val is None:
            return prop, None

        is_lst = prop in MAYBE_LISTS
        if is_lst:           return prop, json.dumps(val or [])
        if val == inf:       return prop, '"Infinity"'
        if typ is bool:      return prop, str(val).lower() if val is not None else "null"
        if typ in (int,str): return prop, json.dumps(val)

        raise NotImplementedError(
            f"Conversion for {prop}:{typ} in {self.__class__.__name__} is not implemented"
        )






class PageConfiguration(Dict[EditorName,IdeConfig]):
    """
    Represent the Configuration for one single page of the documentation (when needed).
    Holds the individual configurations for each IDE in the page, and also the set registering
    the different kinds of ScriptKind that the page will need to work properly.

    The purpose of this kind of object is to be dumped as html later.
    """

    def __init__(self, env):
        super().__init__()
        self.env: PyodideMacrosPlugin = env
        self.needs: Set[ScriptKind] = set()


    def dump_as_scripts(self,
            going_up:str,
            kind_to_scripts:Dict[ScriptKind,str],
            chunks:List[str],
        ):
        """
        Create the <script> tag containing the "global" object to define for all the IDEs in the
        current page, and yield it with all the scripts or css contents to insert in that page.

        @going_up:          Relative path string allowing to retrieve the root level of the docs.
        @kind_to_scripts:   Relations between kinds and the scripts the involve.
        @chunks:            List of slices of the current page. The insertions must be added to it.
        """

        # Yield the global variable first, because the JS scripts will use it at runtime:

        global_var = '{' + ', '.join(
            f'"{ editor_name }": { conf.dump_to_js_code() }' for editor_name,conf in self.items()
        )+'}'
        encoded = compress_LZW(global_var)
        chunks.append(Html.script(f"let PAGE_IDES_CONFIG = { encoded !r}"))

        # Spot invalid kinds:
        missed = {kind for kind in self.needs if kind not in kind_to_scripts}
        if missed:
            logger.error(
                "Some macros are registering the need for these kinds while there are no files "
              + "registered for them:"
              + ''.join(f"\n    { ScriptKind.__name__ }.{ k }" for k in missed)
            )

        # Then register all the scripts and/or css the current page is needing:
        for kind in sorted(self.needs, key=KIND_ORDER.__getitem__):
            insertion = kind_to_scripts[kind].format(to_base=going_up)
            chunks.append(insertion)


    def set(self, editor_name:str, prop:str, value:Any):
        """ Register an IDE configuration property, creating the IdeConfig on the fly,
            if it doesn't exist yet.
        """
        if self.env._dev_mode and prop not in IdeConfig.__annotations__:    # pylint: disable=no-member, protected-access
            msg = f'{prop!r} is not a valide attribut of { IdeConfig.__name__ } class'
            raise AttributeError(msg)

        if editor_name not in self:
            self[editor_name] = IdeConfig()

        setattr(self[editor_name], prop, value)


    def update_kinds(self , kinds:Tuple[ScriptKind]):
        """
        Register a kind of "need" (things to insert in the bottom of the content age, as css or
        scripts) for the current page.
        """
        self.needs.update(kinds)
