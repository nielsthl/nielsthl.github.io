import re, sys
from Macros import Macros


class TokenType:

    def __init__(self, name, rege):
        self.name = name
        self.rege = re.compile(rege)

class Token:

    def __init__(self, type, content):
        self.type = type
        self.content = content

    def __str__(self):
        return "<{type}, {content}>".format(type=self.type.name, content=self.content)

class LexerException(Exception):

    def __init__(self, msg, pos):
        self.msg = msg
        self.pos = pos

    def __str__(self):
        return "Error at position: {pos} - {msg}". format(pos = self.pos, msg = self.msg)

class Lexer(Macros):

#    PARAMETER = TokenType('PARAMETER', r'#[1-9]')
    SYMBOL = TokenType('SYMBOL', r'&')
    BEGINENV = TokenType('BEGINENV', r'\\begin\{([A-Za-z\*]+)\}')
    CONTROLSEQ = TokenType('CONTROLSEQ', r'\\(\\|,|\{|\}|#|%|[A-Za-z*]+)') # Special: '\', ','
    DISPLAYDELIMITER = TokenType('DISPLAYDELIMITER',  r'\$\$')
    ENDENV = TokenType('ENDENV', r'\\end\{([A-Za-z\*]+)\}')
    BEGINGROUP = TokenType('BEGINGROUP', r'\{')
    MATHDELIMITER = TokenType('MATHDELIMITER',  r'\$')
    NEWLINE = TokenType('NEWLINE', r'\n')
    PARAGRAPH = TokenType('PARAGRAPH', r'\n[ \t]*\n\s*') # One blank line = new paragraph
#    PERCENT = TokenType('PERCENT', r'%')
    PERCENT = TokenType('PERCENT', r'%.*[\n|$]')
    ENDGROUP = TokenType('ENDGROUP', r'\}')
    LEFTBRACKET = TokenType('LEFTBRACKET', r'\[')
    RIGHTBRACKET = TokenType('RIGHTBRACKET', r'\]')
    SPACE = TokenType('SPACE', r'[ \t]')
    #WORD = TokenType('WORD', r'[^ \\\{\}\$\%&\n\[\]#]+') # Take care of dangling '#' later
    WORD = TokenType('WORD', r'[^ \\\{\}\$\%&\n\[\]]+') # Take care of dangling '#' later

    # Ordering important below! E.g. DISPLAYDELIMITER must come before MATHDELIMITER
    
    tokenids = (
    PARAGRAPH,
    NEWLINE,
    SPACE,
#    PARAMETER,
    SYMBOL,
    BEGINENV,
    ENDENV,
    CONTROLSEQ,
    BEGINGROUP,
    ENDGROUP,
    LEFTBRACKET,
    RIGHTBRACKET,    
    DISPLAYDELIMITER,
    MATHDELIMITER,
    WORD,
    PERCENT
    )

    def __init__(self, inputstring):
        Macros.__init__(self)
        self.inputstring = inputstring
        self.pos = 0
        self.tok = None
        self.value = None
        self.curtok = None
        self.endofinput = False
        self.tokenlist = []
        self.tokenize()
        self.tokens = iter(self.tokenlist)

    def countlines(self, pos):
        return self.inputstring[:pos].count("\n") + 1


    def getnexttoken(self):
        self.endofinput = False
        try:
            tok = next(self.tokens)
            self.tok = tok.type.name
            self.value = tok.content
        except StopIteration:
            self.endofinput = True
    
    def getnexttok(self):
        if self.pos >= len(self.inputstring):
            self.endofinput = True
            return

        for tok in Lexer.tokenids:
            match = tok.rege.match(self.inputstring, self.pos)
            if match:
                self.tok = tok.name
                self.value = match.group(0)
                self.curtok = Token(tok, self.value)
                self.pos = match.end(0)
                return

        lineno = self.countlines(self.pos)    
        raise LexerException("Unknown token:"+self.inputstring[self.pos: self.pos+10], lineno)



    #
    # Functions at tokenize level:
    #
    # \newcommand, \include{filename}
    #
    # \macros
    #
    # \bye
    #
        
    def tokenize(self):
        self.getnexttok()
        while not self.endofinput:

            if self.iscs("\\newcommand"):
                self.storemacro()
                self.getnexttok()
                continue

            if self.ismacro():
                self.expandmacro()
                self.getnexttok()
                continue

            if self.iscs("\\include"):
                self.includefile()
                self.getnexttok()
                continue
            
            if self.iscs("\\bye"): 
                self.endofinput = True

            self.tokenlist.append(self.curtok)
            self.getnexttok()
