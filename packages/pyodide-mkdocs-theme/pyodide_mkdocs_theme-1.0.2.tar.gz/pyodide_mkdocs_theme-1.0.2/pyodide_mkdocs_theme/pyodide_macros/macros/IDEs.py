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

# pylint: disable=invalid-name, missing-module-docstring


from functools import wraps
from typing import Optional, Type



from ..tools_and_constants import ScriptSection
from ..parsing import build_code_fence
from ..plugin.maestro_IDE import MaestroIDE
from .ide_files_data import IdeFilesExtractor
from .ide_manager import IdeManager
from .ide import Ide
from .ide_terminal import Terminal
from .ide_pybtn import PyBtn





def _IDE_maker(env:MaestroIDE, mode:str, kls:Type[IdeManager], macro_name):

    @wraps(_IDE_maker)
    def wrapped(
        py_name: str = "",
        *,
        ID: Optional[int] = None,
        SANS: str = "",
        WHITE: str = "",
        REC_LIMIT: int = -1,
        **kw
    ) -> str:
        return kls(
            env, py_name, ID, SANS, WHITE, REC_LIMIT,
            mode=mode,      # legacy behavior... Has to be provided.
            extra_kw=kw     # Arguments sink... (None: see IdeManager contract)
        ).make_element()

    wrapped.__name__ = wrapped.__qualname__ = macro_name
    return wrapped




def IDE(env:MaestroIDE):
    """ To build editor+terminal on 2 rows """
    return _IDE_maker(env, "", Ide, "IDE")


def IDEv(env:MaestroIDE):
    """ To build editor+terminal on 2 columns """
    return _IDE_maker(env, "_v", Ide, "IDEv")


def terminal(env:MaestroIDE):
    """ To build an isolated terminal """
    return _IDE_maker(env, "", Terminal, "terminal")


def py_btn(env:MaestroIDE):
    """ To build an isolated button, to run python `env` sections """
    return _IDE_maker(env, "", PyBtn, "py_btn")





def section(env:MaestroIDE):
    """
    Insert the given section from the python file.
    Note: To use only on python scripts holding all the sections for the IDE macros. For regular
          files, use the `py` macro or regular code fences with file inclusions (for performances
          reasons).
    """
    @wraps(section)
    def _section(
        py_name:str,
        section_name:ScriptSection,
        ID=None                         # sink (deprecated)
    ):
        file_data = IdeFilesExtractor(env, py_name)
        content   = file_data.get_section(section_name)
        indent    = env.get_macro_indent()
        out       = build_code_fence(content, indent, lang='python')
        return out

    return _section
