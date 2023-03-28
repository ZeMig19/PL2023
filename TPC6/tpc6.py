import sys
import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'AP',
   'FP',
   'SEP',
   'SLCOMMENT',
   'INT',
   'NUMBER',
   'VARIABLE',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'EQUAL',
   'EL',
   'PROGRAMR'
   'OP',
   'WHILER',
)

states = (
("MLCOMMENT", "exclusive"),
("FUNCTION", "inclusive"),
("WHILE", "inclusive"),
("FOR", "inclusive"),
("PROGRAM", "inclusive"),
)
#
#           MultiLine comment
#
t_MLCOMMENT_ignore  = ''
def t_MLCOMMENT(t):
    r"\/\*([^\*\/])*(\#end)?"
    t.lexer.push_state("MLCOMMENT")
    pass
def t_MLCOMMENT_newline(t):
    r"--[^\*\/]*(\#end)?"
    pass
def t_MLCOMMENT_END(t):
    r" \*\/"
    t.lexer.pop_state()
    pass
def t_MLCOMMENT_error(t):
    print(f"{t.lexer.lineno}, error: wrong MLCOMMENT ")
    exit(1)

# Regular expression rules for simple tokens
t_AP    = r'\['
t_FP   = r'\]'
t_SEP   = r','
t_SLCOMMENT = r'//.*'

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUAL  = r'\='
t_EL  = r'\;'
#
#           INT
#
def t_INT(t):
    r'\s*(int)\s+([a-zA-Z]\w*)\s*([=]\s*(\d+)\s*)?;'
    t.type = 'INT'
    v = lex.LexToken()
    #print(t.lexer.lexmatch.groups())
    v.type = t.lexer.lexmatch.group(6)
    v.lineno = t.lineno
    v.lexpos = t.lexpos
    if t.lexer.lexmatch.group(8) == None:
        v.value = 0
    else:
        v.value = int(t.lexer.lexmatch.group(8))
    t.value = v
    return t
#
#           Function
#
def t_FUNCTION(t):
    r'\s*function\s+[a-zA-Z]\w*\s*\(\s*([a-zA-Z]\w*)*(\s*,\s*([a-zA-Z]\w*)\s*)*\)\s*\{'
    print("t_FUNCTION")
    t.lexer.push_state("FUNCTION")
def t_FUNCTION_END(t):
    r" \s*}"
    print("t_FUNCTION_END")
    t.lexer.pop_state()
def t_FUNCTION_error(t):
    print(f"{t.lexer.lineno}, error: wrong t_FUNCTION_error ")
t_FUNCTION_ignore  = '\n'
#
#           PROGRAM
#
def t_PROGRAM(t):
    r'\s*program\s+([a-zA-Z]\w*)\s*\{'
    t.type = 'PROGRAMR'
    t.value = t.lexer.lexmatch.group(14)
    t.lexer.push_state("PROGRAM")
    #return t
def t_PROGRAM_END(t):
    r" \s*}"
    print("t_PROGRAM_END")
    t.lexer.pop_state()
def t_PROGRAM_error(t):
    print(f"{t.lexer.lineno}, error: wrong t_PROGRAM_error ")
t_PROGRAM_ignore  = '\n'
#
#           While:
#
def t_WHILE(t):
    r'\s*while\s+([a-zA-Z]\w*)\s*(>|>=|<=|<|==|!=)\s*(\w*)\s*{'
    nomeVar = t.lexer.lexmatch.group(16)
    nomeVar_v = lex.LexToken()
    nomeVar_v.value = nomeVar
    nomeVar_v.type = "VARIABLE"
    nomeVar_v.lineno = t.lineno
    nomeVar_v.lexpos = t.lexpos

    op = t.lexer.lexmatch.group(17)
    op_v = lex.LexToken()
    op_v.value = op
    op_v.type = "OP"
    op_v.lineno = t.lineno
    op_v.lexpos = t.lexpos

    seg = t.lexer.lexmatch.group(18)
    seg_v = lex.LexToken()
    seg_v.value = seg
    seg_v.type = "VARIABLE"
    seg_v.lineno = t.lineno
    seg_v.lexpos = t.lexpos

    t.type = 'WHILER'
    t.value = [nomeVar_v,op_v,seg_v]
    t.lexer.push_state("WHILE")
    return t
def t_WHILE_END(t):
    r" \s*}"
    print("t_WHILE_END")
    t.lexer.pop_state()
def t_WHILE_error(t):
    print(f"{t.lexer.lineno}, error: wrong t_WHILE_error ")
t_WHILE_ignore  = ' \n'
#
#           For:
#
def t_FOR(t):
    r'\s*for\s+[a-zA-Z]\w*\s+in\s+\[\s*\d+\s*..\s*\d+\s*\]\s*{'
    print("t_FOR")
    t.lexer.push_state("FOR")
def t_FOR_END(t):
    r" \s*}"
    print("t_FOR_END")
    t.lexer.pop_state()
def t_FOR_error(t):
    print(f"{t.lexer.lineno}, error: wrong t_FOR_error ")
t_FOR_ignore  = ' \n'

#
#           Expression
#
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_num(p):
    'factor : VARIABLE'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

#
#           Igualdade
#
def p_igualdade(p):
    'VARIABLE EQUAL expression EL'
    p[0] = p[1]


def t_VARIABLE(t):
    r'[a-zA-Z]\w*'
    t.value = str(t.value)    
    return t

def t_NUMBER(t):
    r'\d+'
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
        print(f"{line_number}: {line}")
        lexer.input(line)
        line_number = line_number + 1
        for token in lexer:
            print("Token = " + str(token))


if __name__ == "__main__":
    main()