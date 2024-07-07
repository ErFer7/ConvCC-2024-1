"""
Símbolos da gramática.
"""

from enum import Enum


class Terminal(Enum):
    """
    Terminais.
    """

    IDENT = "ident"
    OPEN_P = "("
    CLOSE_P = ")"
    OPEN_SB = "["
    CLOSE_SB = "]"
    OPEN_CB = "{"
    CLOSE_CB = "}"
    COMMA = ","
    SEMICOLON = ";"
    MULTIPLY = "*"
    DIVISION = "/"
    REMAINDER = "%"
    ADDITION = "+"
    SUBTRACT = "-"
    ASSIGNMENT = "="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    EQUAL = "=="
    NOT_EQUAL = "!="
    DEF = "def"
    NEW = "new"
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    PRINT = "print"
    READ = "read"
    RETURN = "return"
    BREAK = "break"
    IF = "if"
    ELSE = "else"
    FOR = "for"
    INT_CONST = "int_const"
    FLOAT_CONST = "float_const"
    STRING_CONST = "string_const"
    NULL_CONST = "null"
    AND = "and"
    OR = "or"
    NOT = "not"
    CALL = "call"


class NonTerminalType(Enum):
    """
    Não terminal.
    """

    PROGRAM = "PROGRAM"
    FUNCLIST = "FUNCLIST"
    MOREFUNCS = "MOREFUNCS"
    FUNCDEF = "FUNCDEF"
    PARAMLIST = "PARAMLIST"
    PARAMETER = "PARAMETER"
    MAYBEPARAMS = "MAYBEPARAMS"
    TYPE_DECL = "TYPE_DECL"  # type
    STATEMENT = "STATEMENT"
    VARDECL = "VARDECL"
    ARRAYSIZE = "ARRAYSIZE"
    ATRIBSTAT = "ATRIBSTAT"
    ATRIBEXPR = "ATRIBEXPR"
    FUNCCALL = "FUNCCALL"
    PARAMLISTCALL = "PARAMLISTCALL"
    SOCALLMEMAYBE = "SOCALLMEMAYBE"
    PRINTSTAT = "PRINTSTAT"
    READSTAT = "READSTAT"
    RETURNSTAT = "RETURNSTAT"
    IFSTAT = "IFSTAT"
    MAYBEELSE = "MAYBEELSE"
    FORSTAT = "FORSTAT"
    STATELIST = "STATELIST"
    MAYBESTATELIST = "MAYBESTATELIST"
    ALLOCEXPRESSION = "ALLOCEXPRESSION"
    INDEXEXPRESSION = "INDEXEXPRESSION"
    EXPRESSION = "EXPRESSION"
    MAYBECOMPARE = "MAYBECOMPARE"
    COMPARISON = "COMPARISON"
    NUMEXPRESSION = "NUMEXPRESSION"
    INDEXTERM = "INDEXTERM"
    TERM = "TERM"
    MULTUNARY = "MULTUNARY"
    MULDIV = "MULDIV"
    ADDSUB = "ADDSUB"
    UNARYEXPR = "UNARYEXPR"
    FACTOR = "FACTOR"
    LVALUE = "LVALUE"



STRING_TO_TERMINAL = {member.value: member for member in Terminal}

# Terminais que são definitivos com um único caractere e não são o começo de outro terminal maior
ONE_CHAR_DEFINITIVE_TERMINALS = [
    Terminal.OPEN_P,
    Terminal.CLOSE_P,
    Terminal.OPEN_SB,
    Terminal.CLOSE_SB,
    Terminal.OPEN_CB,
    Terminal.CLOSE_CB,
    Terminal.COMMA,
    Terminal.SEMICOLON,
    Terminal.MULTIPLY,
    Terminal.DIVISION,
    Terminal.REMAINDER,
    Terminal.ADDITION,
    Terminal.SUBTRACT,
]


class NonTerminal:
    """
    Não terminal.
    """

    _type: NonTerminalType
