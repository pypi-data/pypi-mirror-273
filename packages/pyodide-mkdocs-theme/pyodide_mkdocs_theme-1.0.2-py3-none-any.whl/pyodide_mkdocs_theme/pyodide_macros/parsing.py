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


from pathlib import Path
import re
from typing import Callable, List, Optional
from string import printable
from random import shuffle

from mkdocs.exceptions import BuildError

from .exceptions import PyodideMacrosParsingError
from .tools_and_constants import LZW, DebugConfig





def replace_chunk(source:str, start:str, end:str, repl:str, *, at=0, keep_limiters=False):
    """ Given a @source and two delimiters/tokens, @start and @end, find those two tokens in
        @source, then replace the content of source between those two tokens with @repl.

        @at=0:                  Starting point for the search of @start in @source.
        @keep_limiters=False:   If True, the @start and @end tokens are kept and @repl is
                                placed in between them instead.
    """
    i,j = eat(source, start, at)
    _,j = eat(source, end,   j)
    if keep_limiters:
        repl = start + repl + end
    return source[:i] + repl + source[j:]


def eat(source:str, token:str, start=0, *, skip_error=False):
    """ Given a @source text, search for the given @token and returns the indexes locations
        of it, i and j (i: starting index, j: ending index, exclusive, as for slicing).

        @start=0:           Starting index for the search
        @skip_error=False:  Raises ValueError if False and the token isn't found.
                            If True and the token isn't found, returns i=j=len(source).
    """
    i = source.find(token, start)
    if i>=0:
        return i, i+len(token)

    if skip_error:
        return len(source), len(source)

    # handle error message:
    end  = min(1000, len(source)-start)
    tail = "" if end != 1000 else ' [...]'
    raise ValueError(f"Couldn't find {token=} in:\n\t[...] {source[start:end]}{ tail }")







def camel(snake:str):
    """ Transform a snake_case python property to a JS camelCase one. """
    snake = re.sub(r'_{2,}', '_', snake)
    return re.sub(r'(?<=[a-zA-Z\d])_([a-z\d])', _camelize, snake)

def _camelize(m:re.Match):
    return m[1].upper()


def items_comma_joiner(lst:List[str], join:str):
    """ ['1','2','3','4']  -> '1, 2, 3 {join} 4' """
    elements = lst[:]
    if len(elements)>1:
        last = elements.pop()
        elements[-1] += f" {join} {last}"
    elements = ', '.join(elements)
    return elements





# MEAN = []

# def encrypt_string(text, key = 43960):
#     """ Applique c ^ 43960 à chaque caractère de text (43960 = 0b1010101010101010) and send that
#         as dot joined integers (needed to allow JS to decode emojis "the way python sees them")
#         (...sort of...)
#     """
#     out = ".".join( f"{ c^key :0>5}" for c in map(ord,text) )
#     MEAN.append((len(text),len(out)))
#     return out






TOME_BASE = re.sub(r'[<>"\[\]\\]', '', printable)[:-5]
""" Removed:
        - "<>" because could generate tags
        - "[]" because could be seen as md links syntaxe by mkdocs-addresses
"""
BASE = len(TOME_BASE)


def i_to_base(n,size):
    out = ''.join(
        TOME_BASE[ n // BASE**p % BASE ]
        for p in reversed(range(size))
    )
    if n != un_i_to_base(out):
        raise
    return out

def compress_LZW(txt:str):
    return txt
    # print(txt)

    tome  = set(txt) - set('<>')                    # remove tags tokens
    big   = list(filter(chr(255).__lt__, tome))     # might be problematic for python->JS transfer
    small = list(filter(chr(255).__ge__, tome))     # easy ones (python->JS)
    if DebugConfig.shuffle:
        shuffle(small)                              # 'cause, why not... :p
    alpha = list('><')+big+small                    # Will always be added afterward

    def grab(j):
        i,j = j,j+1
        while j<len(txt) and txt[i:j] in dct: j+=1
        token = txt[i:j]

        if token not in dct:
            # tokens.append(token)
            dct[token] = i_to_base(len(dct), size)
            return j-1, dct[token[:-1]]

        return len(txt), dct[token]

    out,i,size,limit = [], 0, 2, BASE**2
    dct = {c: i_to_base(i, size) for i,c in enumerate(alpha)}
    # tokens = [*alpha]

    while i < len(txt):
        i,idx_base = grab(i)
        out.append(idx_base)
        if len(dct)==limit:     # Reached x**base-1 => increase the chunk size
            out.append(LZW)
            size += 1
            limit = BASE**size

    # Each \n char in the encoded tag means "increase the token byte length by one"
    # print(table)
    # print('dict size:',len(dct), 'size:', size)
    # print(len(src_txt),'->',len(output))
    # rev_table = {s:i for i,s in enumerate(table)}
    # counts = [tokens[rev_table[s]] for s in out]
    # print('---',*Counter(counts).most_common(),'---', sep='\n')

    # version to put in the encoded tag, WITHOUT any "<" or ">" character:
    encoded_bigs      = '.'.join( str(ord(c)) for c in big )
    encoded_smalls    = ''.join(small)
    output_with_table = f".{ encoded_bigs }{ LZW }{ encoded_smalls }{ LZW }{ ''.join(out) }"
    # Extra leading dot to allow unconditional trim in JS, later...

    if DebugConfig.check_decode:
        decoded = decode_LZW(output_with_table)
        if decoded != txt:
            alpha = ''.join(sorted(set(txt)))
            i = next(
                (i for i,(a,b) in enumerate(zip(txt,decoded)) if a!=b),
                min(len(txt), len(decoded))
            )
            (Path.cwd() / "encoded").write_text(output_with_table.replace('\x1e', '\n'), encoding='utf-8')
            raise BuildError(f'''Failed to decode...
Alpha: ]]{ alpha }[[ (len={len(alpha)})
        { [*map(ord,alpha)] }

table: len={len(dct)}
{size=} | BASE**size = {BASE**size}

source: len={len(txt)}
back:   len={len(decoded)}
Differ: {i=}

source[i-50:i]:
{ txt[i-50:i] }

source[i:i+200]:
{ txt[i:i+200]}

source[i:i+200]:
{decoded[i:i+200]}

''')


    # MEAN.append((len(txt),len(out)))
    return output_with_table



BASE_TOME = {c:i for i,c in enumerate(TOME_BASE)}
def un_i_to_base(s:str):
    v = 0
    for c in s: v = BASE*v + BASE_TOME[c]
    return v


def decode_LZW(compressed:str):

    big,small,*chunks = compressed.strip().split(LZW)
    big = big[1:]
    tome = [*'><'] + [chr(int(s)) for s in big and big.split('.')] + [*small]

    txt,size = [],1
    for chunk in chunks:
        size += 1
        assert not len(chunk)%size, (len(chunk), size, len(chunk)%size)
        txt.extend( un_i_to_base(chunk[i:i+size]) for i in range(0, len(chunk), size) )

    out = []
    for i,idx in enumerate(txt):
        w = tome[idx]
        fresh = '' if i+1==len(txt) else w + ( w if txt[i+1]==len(tome) else tome[txt[i+1]] )[0]
        # https://mooc-forums.inria.fr/moocnsi/t/question-lzw-cas-particulier-decompression/11491/2
        out.append(w)
        tome.append(fresh)

    return ''.join(out)






def build_code_fence(
    content:str,
    indent:str="",
    line_nums=1,
    lang:str='python',
    title:str=""
) -> str :
    """
    Build a markdown code fence for the given content and the given language.
    If a title is given, it is inserted automatically.
    If linenums is falsy, no line numbers are included.
    If @indent is given each line is automatically indented.

    @content (str): code content of the code block
    @indent (str): extra left indentation to add on each line
    @line_nums (=1): if falsy, no line numbers will be added to the code block. Otherwise, use
                     the given int value as starting line number.
    @lang (="python"): language to use to format the resulting code block.
    @title: title for the code block, if given. Note: the title cannot contain quotes `"`
    """
    line_nums = f'linenums="{ line_nums }"' if line_nums else ""
    if title:
        if '"' in title:
            raise BuildError(
                f'Cannot create a code fence template with a title containing quotes:\n'
                f"  {lang=}, {title=!r}\n{content}"
            )
        title = f'title="{ title }"'

    lst = [
        '',
        f"```{ lang } { title } { line_nums }",
        *content.strip('\n').splitlines(),
        "```",
        '',
    ]
    out = '\n'.join( indent+line for line in lst )
    return out












class IndentParser:
    """
    Build a markdown parser class, extracting the indentations of macros calls requiring
    indentation, and taking in consideration jinja markups (skip {% raw %}...{% endraw %},
    properly parse complex macro calls, ignore macro variables).

    The result of the method `IndentParser(content).parse()` is a list of `Tuple[str,int]`:
    `(macro_name, indent)`, in the order they showed up in the content.
    """

    STR_DECLARATIONS = '"""', "'''", '"', "'"
    EXTRAS_TOKENS    = [r'\w+', r'\n', r'[\t ]+', r'\\', '.']

    __CACHE = {}

    def __init__(self,
        open_block:str,
        close_block:str,
        open_var:str,
        close_var:str,
        is_macro_with_indent:Callable[[str],bool],
    ):
        self.is_macro_with_indent = is_macro_with_indent

        # Build the delimiters according to the user config of the MacrosPlugin:
        self.open_block  = open_block
        self.close_block = close_block
        self.open_var    = open_var
        self.close_var   = close_var
        self.open_raw    = f'{open_block} raw {close_block}'
        self.close_raw   = f'{open_block} endraw {close_block}'
        self.pairs       = {}

        # Defined in self.parse(...):
        self.src_file = None
        self.i        = 0
        self.tokens   = []
        self.indents  = []
        self.current  = None        # current macro call


        raw_open_close = [
            [self.open_raw, self.close_raw],
            [open_block,    close_block],
            [open_var,      close_var],
            *( [s,s] for s in self.STR_DECLARATIONS),
            ['(', ')'],
            ['[', ']'],
            ['{', '}'],
        ]
        tokens = []
        for o,c in raw_open_close:
            self.pairs[o] = c
            tokens += [o,c]

        tokens.sort(key=len, reverse=True)

        self.pattern = re.compile('|'.join(
            [re.escape(s).replace('\\ ',r'\s*') for s in tokens] + self.EXTRAS_TOKENS
        ), flags=re.DOTALL)



    def parse(self, content:str, src_file=None):
        """
        Parse the given content and extract all the indentation levels for each macro call
        identified as being a "macro_with_indent".

        - Returns a copy of the result.
        - Results are cached in between builds.
        """
        # pylint: disable=attribute-defined-outside-init
        self.src_file = src_file

        if content not in self.__CACHE:
            self.i = 0
            self.tokens = self.pattern.findall(content)
            self.indents = []

            while self.i < len(self.tokens):
                tok = self._eat()
                if   tok == self.open_var:     self._gather_jinja_var()
                elif tok == self.open_raw:     self._eat_until(self.close_raw)
                elif tok == self.open_block:   self._eat_until(self.close_block)

            self.__CACHE[content] = self.indents

        return self.__CACHE[content][:]


    #-------------------------------------------------------------
    #                       Error feedback
    #-------------------------------------------------------------


    def __extract(self, I, di):
        i,j = (I+di, I) if di<0 else  (I+1, I+1+di)
        a,b = (0,-1) if di<0 else (1,None)
        return repr( ''.join(self.tokens[i:j]) )[a:b]


    def __location_info(self, tok, i:Optional[int]=None):
        i = self.i if i is None else i
        return f"{ self.__extract(i,-10) }\033[31m>>{tok}<<\033[0m{ self.__extract(i,10) }"


    def _error_info(self, info:str, tok:str):
        macro = ''
        indents = "No indents found so far."

        if self.current:
            i,msg = self.current
            macro = (
                f"\nMacro being parsed during the error (index : { i }/{ len(self.tokens) }):\n"
                f"    { msg }\n"
            )
        if self.indents:
            indents = "\nKnown indents so far: " + ''.join(
                f"\n\t{name}: {n}" for name,n in self.indents
            )

        return (
            "Parsing error while looking for macro calls indentation data.\n"
            "The parser might EOF when strings in a macro call are improperly written, so double "
            "check there are no unescaped delimiters inside strings used in the macro call.\n"
            f"With \033[31m>>tok<<\033[0m denoting the tokens of interest:\n\n"
            f"\033[34m{ info }, in { self.src_file }\033[0m\n{ macro }\n"
            f"Tokens around the error location (index: { self.i }/{ len(self.tokens) }):\n"
            f"    { self.__location_info(tok) }\n"
            f"\n{ indents }"
        )


    #-------------------------------------------------------------
    #                     Parsing machinery
    #-------------------------------------------------------------


    def _taste(self):
        return self.tokens[self.i] if self.i<len(self.tokens) else None

    def _eat(self,reg:str=None, msg:str=None):
        tok = self._taste()
        if tok is None or reg is not None and not re.fullmatch(reg, tok):
            tok = 'EOF' if tok is None else repr(tok)
            reg = reg or msg
            msg = 'Reached EOF' if not reg else f'Expected pattern was: {reg!r}, but found: {tok}'
            raise PyodideMacrosParsingError( self._error_info(msg, tok) )
        self.i+=1
        return tok

    def _walk(self):
        while True:
            tok = self._taste()
            if not tok or not tok.isspace(): return
            self.i += 1

    def _eat_until(self, target, apply_backslash=False):
        while True:
            tok = self._eat(msg=target)
            if tok==target:
                return
            elif tok=='\\' and apply_backslash: self._eat()



    def _consume_code(self, target:str):
        while True:
            tok = self._eat(msg=target)
            if tok==target:
                break
            elif tok in self.pairs:
                is_str_declaration = tok in self.STR_DECLARATIONS
                closing = self.pairs[tok]
                if is_str_declaration:
                    self._eat_until(closing, True)
                else:
                    self._consume_code(closing)


    def _gather_jinja_var(self):
        start = self.i-1        # index of the '{{' token, to compute indentation later
        self._walk()
        i_name = self.i
        name = self._eat(r'\w+')
        self._walk()
        tok = self._taste()
        is_macro = tok=='('

        self.current = i_name, self.__location_info(name, i_name)
        if is_macro and self.is_macro_with_indent(name):
            self._store_macro_with_indent(start, name)
            self._eat()
            self._consume_code(')')

        self._consume_code(self.close_var)


    def _store_macro_with_indent(self, start:int, name:str):
        i = max(0, start-1)
        while i>0 and self.tokens[i].isspace() and self.tokens[i] != '\n':
            i -= 1

        tok = self.tokens[i]
        if i and tok not in ('\n',self.open_var):
            raise PyodideMacrosParsingError( self._error_info(
                f"Invalid macro call:\nThe {name!r} macro is a `macros_with_indents` "
                 "but a call to it has been found with characters on its left. This is "
                f"not possible.\nThis happened", tok)
            )

        i += tok=='\n'
        indent = len(''.join(self.tokens[i:start]))
        self.indents.append( (name,indent) )
