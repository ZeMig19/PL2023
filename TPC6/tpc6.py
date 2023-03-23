import sys
import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'NUM',
   'AP',
   'FP',
   'SEP'
)

states = (
("COMMENT", "exclusive"),
)

t_COMMENT_ignore  = ''

def t_COMMENT(t):
    r"\/\*([^\*\/])*(\#end)?"
    t.lexer.push_state("COMMENT")
    print("t_COMMENT")

def t_COMMENT_newline(t):
    r"--[^\*\/]*(\#end)?"
    print("t_COMMENT_newline")

def t_COMMENT_END(t):
    r" \*\/"
    t.lexer.pop_state()
    print("t_COMMENT_end")

def t_COMMENT_error(t):
    print(f"{t.lexer.lineno}, error: wrong comment ")

# Regular expression rules for simple tokens
t_AP    = r'\['
t_FP   = r'\]'
t_SEP   = r','

# A regular expression rule with some action code
def t_NUM(t):
    r'[+\-]?\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    global line_number
    print(f"{t.lexer.lineno}, error: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def main():
    lexer = lex.lex()
    line_number = 0
    for line in sys.stdin:
        lexer.input(line)
        for tok in lexer:
            print(f"{tok.lineno}: {line}")


if __name__ == "__main__":
    main()