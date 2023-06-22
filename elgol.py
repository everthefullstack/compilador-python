import sys
import ply.yacc as yacc
import ply.lex as lex
from utils import create_txt

# Lista de palavras reservadas.
reserved = {
    "elgio": "ELGIO",
    "inteiro": "INTEIRO",
    "zero": "ZERO",
    "enquanto": "ENQUANTO",
    "se": "SE",
    "entao": "ENTAO",
    "senao": "SENAO",
    "inicio": "INICIO",
    "fim": "FIM",
    "maior": "MAIOR",
    "menor": "MENOR",
    "igual": "IGUAL",
    "diferente": "DIFERENTE",
}

# Lista de nomes de tokens.
#Segundo a documentação, é necessário fazer a concatenação dos tokens e palavras reservadas
tokens = [
    "MAIS",
    "MENOS",
    "VEZES",
    "DIVIDE",
    "ATRIBUI",
    "ID",
    "NUM",
    "FUNCAO",
    "PAR_DIR",
    "PAR_ESQ",
    "FIM_EXP"
] + list(reserved.values())

# Regras de expressão regular para tokens simples
t_MAIS = r'\+'
t_MENOS = r'-'
t_VEZES = r'\bx\b'
t_DIVIDE = r'/'
t_ATRIBUI = r'='
t_PAR_ESQ = r"\("
t_PAR_DIR = r"\)"
t_ignore = " \t" #ignora espaços em branco, tem que ser assim vide documentação do PLY

# Regra de expressão regular com algum código de ação para cada token
def t_ID(t):
    r'[A-Z]{1}[a-z]{2,}'
    t.value = t.value
    return t

def t_NUM(t):
    r'[1-9]\d*'
    t.value = int(t.value)
    return t

def t_FUNCAO(t):
    r'_{1}[A-Z]{1}[a-z]{2,}'
    return t

def t_FIM_EXP(t):
    r'[.]'
    return t

def t_ELGIO(t):
    r'\belgio\b'
    return t

def t_INTEIRO(t):
    r'\binteiro\b'
    return t

def t_ZERO(t):
    r'\bzero\b'
    return t

def t_ENQUANTO(t):
    r'\benquanto\b'
    return t

def t_SE(t):
    r'\bse\b'
    return t

def t_ENTAO(t):
    r'\bentao\b'
    return t

def t_SENAO(t):
    r'\bsenao\b'
    return t

def t_INICIO(t):
    r'\binicio\b'
    return t

def t_FIM(t):
    r'\bfim\b'
    return t

def t_MAIOR(t):
    r'\bmaior\b'
    return t

def t_MENOR(t):
    r'\bmenor\b'
    return t

def t_IGUAL(t):
    r'\bigual\b'
    return t

def t_DIFERENTE(t):
    r'\bdiferente\b'
    return t   

# Ignora comentários de linha
def t_COMMENT(t):
    r'\#.*'
    pass

# Regra que consegue rastrear numero de linha
def t_NOVA_LINHA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra de tratamento de erros mostrando a linha e a coluna
def t_error(t):

    print(f"Caractere ilegal -> {t.value[0]}")
    print(f"linha: {t.lexer.lineno} posição: {find_column(t)}\n")

def find_column(token):
    # Obtém o texto completo do token
    input_text = token.lexer.lexdata

    # Obtém a posição da última quebra de linha no texto completo
    last_br = input_text.rfind('\n', 0, token.lexpos)

    # retorna -1 se não encontrar quebra de linha
    # se não tem quebra de linha, então é a primeira linha
    if last_br < 0:
        last_br = 0
    
    #a posição do token - a posição da última quebra de linha fornece a coluna
    return token.lexpos - last_br

def p_error(p):
    print(f"Syntax error in input! {p}")

def p_start(p):
    """start : expr
    """
    p[0] = p[1]

def p_expr(p):
    """expr : tipo_var
            | atribuicao
            | se
            | entao
            | inicio
            | fim
            | soma
            | subtracao
            | multiplicacao
            | divisao
    """
    p[0] = p[1]

def p_tipo_var(p):
    """tipo_var : tipo var FIM_EXP
                | tipo var FIM_EXP start
    """
    p[0] = p[1]

def p_tipo(p):
    """tipo : INTEIRO
    """
    p[0] = p[1]

def p_var(p):
    """var : ID 
    """
    p[0] = p[1]

def p_num(p):
    """num : NUM
           | ZERO
    """
    if p[1] == "zero":
        p[0] = 0

    else:
        p[0] = p[1]

def p_atribuicao(p):
    """atribuicao : var ATRIBUI var FIM_EXP
                  | var ATRIBUI num FIM_EXP
                  | var ATRIBUI var FIM_EXP start
                  | var ATRIBUI num FIM_EXP start
    """
    p[0] = p[3]

def p_se(p):
    """se : SE var logicos var FIM_EXP
          | SE num logicos num FIM_EXP
          | SE num logicos var FIM_EXP
          | SE var logicos num FIM_EXP
          | SE var logicos var FIM_EXP start
          | SE num logicos num FIM_EXP start
          | SE num logicos var FIM_EXP start
          | SE var logicos num FIM_EXP start
    """

def p_logicos(p):
    """logicos : MAIOR
               | MENOR
               | IGUAL
               | DIFERENTE
    """
    if p[1] == "maior":
        p[0] = ">"
    
    elif p[1] == "menor":
        p[0] = "<"
    
    elif p[1] == "igual":
        p[0] = "=="
    
    elif p[1] == "diferente":
        p[0] = "!="

def p_entao(p):
    """entao : ENTAO FIM_EXP
             | ENTAO FIM_EXP start
    """

def p_inicio(p):
    """inicio : INICIO FIM_EXP
              | INICIO FIM_EXP start
    """

def p_fim(p):
    """fim : FIM FIM_EXP
           | FIM FIM_EXP start
    """

def p_soma(p):
    """soma : var MAIS var FIM_EXP
            | var MAIS num FIM_EXP
            | num MAIS num FIM_EXP
            | var MAIS var FIM_EXP start
            | var MAIS num FIM_EXP start
            | num MAIS num FIM_EXP start
    """
    p[0] = p[1] + p[3]
    print(p[0])
    
def p_subtracao(p):
    """subtracao : var MENOS var FIM_EXP
                 | var MENOS num FIM_EXP
                 | num MENOS num FIM_EXP
                 | var MENOS var FIM_EXP start
                 | var MENOS num FIM_EXP start
                 | num MENOS num FIM_EXP start
    """
    p[0] = p[1] - p[3]

def p_multiplicacao(p):
    """multiplicacao : var VEZES var FIM_EXP
                     | var VEZES num FIM_EXP
                     | num VEZES num FIM_EXP
                     | var VEZES var FIM_EXP start
                     | var VEZES num FIM_EXP start
                     | num VEZES num FIM_EXP start
    """
    p[0] = p[1] * p[3]

def p_divisao(p):
    """divisao : var DIVIDE var FIM_EXP
               | var DIVIDE num FIM_EXP
               | num DIVIDE num FIM_EXP
               | var DIVIDE var FIM_EXP start
               | var DIVIDE num FIM_EXP start
               | num DIVIDE num FIM_EXP start
    """
    p[0] = p[1] / p[3]

# Dados lidos
dados1 = open(sys.argv[1], encoding="utf-8")
dados2 = open(sys.argv[1], encoding="utf-8")

# Constrói o lexer
lexer1 = lex.lex()
lexer2 = lex.lex()
lexer1.input(dados1.read())
lexer2.input(dados2.read())

#Constrói o parser
parser = yacc.yacc()
result = parser.parse(lexer=lexer1, debug=False)
