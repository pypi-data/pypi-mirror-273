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


import re
from typing import Dict, List, Optional, Tuple
from functools import wraps


from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from mkdocs.exceptions import BuildError


from ..exceptions import PyodideConfigurationError
from ..tools_and_constants import MACROS_WITH_INDENT
from ..pyodide_logger import logger
from ..deprecation import deprecation_warning
from ..parsing import IndentParser
from .maestro_base import BaseMaestro



# pylint: disable-next=pointless-string-statement, line-too-long
'''
- Macros are run in "reading order" of the original document, included content also being use this way => fully predictable
- WARNING with md_include, which interleave other calls in the "current context"... => need an external md page parser
- Process:
    1. remove raw markers. NOTE: nested raw markups aren't allowed => easy
    2. tokenize (longest tokens first)
    3. _carefully parse the thing... _ keeping in mind that the input is md text, not actual python...
       and store the indents of the calls to multiline macros in a reversed stack (store a pari indent/macro name,
       to enforce validity of executions on usage)
    4. each time a macro starts running (spotted through the custom macro decorator), pop the current indent to use,
       AND STACK IT , because of potential nested macro calls: A(BCD) => when going back to A, there is no way
       to know if the macro will reach for the indentation value of A, for example.
       Each time the macro returns, pop the current indent from the second stack
    5. for nested macro, add the included indentation data on top of the current reversed stack
'''







class MaestroIndent(BaseMaestro):
    """ Manage Indentation logistic """


    # _pages_indents: 'PageIndents'
    # """
    # Cache storing the indentations for each jinja/macro template in a Page.
    # A page is entirely studied the first time it's seen and the result of the indentation levels
    # are stored.
    # The data stays correct throughout the md->html conversion because the indentation levels
    # "horizontal") are not affected by the content growing ("vertical").
    # """

    _running_macro: Optional[str] = None
    """
    Name of the macro currently running (or the last one called. None if no macro called yet).
    """

    _parser: IndentParser
    _indents_store: List[Tuple[str,int]]
    _indents_stack: List[str]


    def on_config(self, config:MkDocsConfig):

        nope = [ w for w in self.macros_with_indents if not w.isidentifier() ]
        if nope:
            raise PyodideConfigurationError(
                "Invalid macros_with_indents option: should be a of identifiers, but found: "
                f"{ ', '.join(map(repr,nope)) }"
            )

        macros = MACROS_WITH_INDENT.split() + self.macros_with_indents
        self._macro_with_indent_pattern = re.compile('|'.join(macros))

        self._parser = IndentParser(
            self.j2_block_start_string    or "{%",
            self.j2_block_end_string      or "%}",
            self.j2_variable_start_string or "{{",
            self.j2_variable_end_string   or "}}",
            self.is_macro_with_indent,
        )

        super().on_config(config)     # MacrosPlugin is actually "next in line" and has the method



    def on_page_markdown(
        self,
        markdown:str,
        page:Page,
        config:MkDocsConfig,
        site_navigation=None,
        **kwargs
    ):
        indentations = self._parser.parse(markdown, self.location(page))
        self._indents_store = [*reversed(indentations)]
        self._indents_stack = []

        return super().on_page_markdown( markdown, page, config, site_navigation=site_navigation, **kwargs)



    #----------------------------------------------------------------------------



    # Override MacroPlugin
    def macro(self, func, name=""):     # pylint: disable=arguments-renamed
        """
        Add an extra wrapper around the macro, so that it gathers automatically the name of
        the macro currently running (for better error messages).
        """
        name = name or func.__name__

        @wraps(func)
        def wrapper(*a,**kw):
            self._running_macro = name
            need_indent = self.is_macro_with_indent(name)
            if need_indent:
                call,indent = self._indents_store.pop()
                if call != name:
                    raise BuildError(
                        f"Invalid indentation data: expected a call to {call}, but was {name}"
                    )
                self._indents_stack.append(indent * ' ')
            out = func(*a,**kw)
            if need_indent:
                self._indents_stack.pop()

            return out

        wrapper.__name__ = wrapper.__qualname__ = name
        return super().macro(wrapper, name)




    def is_macro_with_indent(self, macro_call:str) -> bool:
        """
        Return True if the given macro call requires to register indentation data.
        This is using a white list, so that user defined macro cannot cause troubles.
        """
        return bool(self._macro_with_indent_pattern.fullmatch(macro_call))


    def get_macro_indent(self):
        """
        Extract the indentation level for the current macro call.
        """
        if not self._indents_stack:
            raise BuildError(f"No indentation available in page { self.location() }")
        return self._indents_stack[-1]


    def get_indent_in_current_page(self, _:re.Pattern=None):
        """
        Extract the indentation needed for the given macro template call.
        @throws:    BuildError if the same macro call is found several times in the page.
        """
        deprecation_warning(
            "Deprecated usage of PyodideMacrosPlugin.get_indent_in_current_page.\n"
            "The get_macro_indent method should be used instead."
        )
        return self.get_macro_indent()
