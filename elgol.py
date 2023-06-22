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


def p_expr(p):
    """expr : var
            | tipo
            | tipo_var
            | atribui
            | se
            | entao
            | inicio
            | fim
    """

def p_var(p):
    """var : ID 
           | ID FIM_EXP
    """


def p_tipo(p):
    """tipo : INTEIRO
    """

def p_tipo_var(p):
    """tipo_var : expr expr
    """
    
def p_num(p):
    """num : NUM
           | ZERO
           | NUM FIM_EXP
           | ZERO FIM_EXP
    """

def p_atribui(p):
    """atribui : expr ATRIBUI expr
               | expr ATRIBUI num
    """
    p[0] = p[3]

def p_logicos(p):
    """logicos : MAIOR
               | MENOR
               | IGUAL
               | DIFERENTE
    """

def p_se(p):
    """se : SE expr logicos expr
          | SE num logicos num
          | SE num logicos expr
          | SE expr logicos num
    """

def p_entao(p):
    """entao : ENTAO FIM_EXP
    """

def p_inicio(p):
    """inicio : INICIO FIM_EXP
    """

def p_fim(p):
    """fim : FIM FIM_EXP
    """

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
result = parser.parse(lexer=lexer1)

print(result)
create_txt(lexer2)