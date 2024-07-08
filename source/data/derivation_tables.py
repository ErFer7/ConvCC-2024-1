from data.grammar import NonTerminalType as N, Terminal as T
from data.semantic_actions import semantic_actions_dict


class Derivation:
    def __init__(self, head: N, tail: list):
        self.head = head
        self.tail = tail


ProductionList = {
    1: Derivation(N.PROGRAM, [N.STATEMENT]),
    2: Derivation(N.PROGRAM, [N.FUNCLIST]),
    3: Derivation(N.PROGRAM, []),
    4: Derivation(N.FUNCLIST, [N.FUNCDEF, N.MOREFUNCS]),
    5: Derivation(N.MOREFUNCS, [N.FUNCLIST]),
    6: Derivation(N.MOREFUNCS, []),
    7: Derivation(
        N.FUNCDEF,
        [
            T.DEF,
            T.IDENT,
            T.OPEN_P,
            N.PARAMLIST,
            T.CLOSE_P,
            T.OPEN_CB,
            N.STATELIST,
            T.CLOSE_CB,
        ],
    ),
    8: Derivation(N.PARAMLIST, [N.TYPE_DECL, N.PARAMETER]),
    9: Derivation(
        N.PARAMETER,
        [T.IDENT, N.MAYBEPARAMS],
    ),
    10: Derivation(N.MAYBEPARAMS, [T.COMMA, N.PARAMLIST]),
    11: Derivation(N.MAYBEPARAMS, []),
    12: Derivation(N.TYPE_DECL, [T.INT]),
    13: Derivation(N.TYPE_DECL, [T.FLOAT]),
    14: Derivation(N.TYPE_DECL, [T.STRING]),
    15: Derivation(N.STATEMENT, [N.VARDECL, T.SEMICOLON]),
    16: Derivation(N.STATEMENT, [N.ATRIBSTAT, T.SEMICOLON]),
    17: Derivation(N.STATEMENT, [N.PRINTSTAT, T.SEMICOLON]),
    18: Derivation(N.STATEMENT, [N.READSTAT, T.SEMICOLON]),
    19: Derivation(N.STATEMENT, [N.RETURNSTAT, T.SEMICOLON]),
    20: Derivation(N.STATEMENT, [N.IFSTAT]),
    21: Derivation(N.STATEMENT, [N.FORSTAT]),
    22: Derivation(N.STATEMENT, [T.OPEN_CB, N.STATELIST, T.CLOSE_CB]),
    23: Derivation(N.STATEMENT, [T.BREAK, T.SEMICOLON]),
    24: Derivation(N.STATEMENT, [T.SEMICOLON]),
    25: Derivation(N.VARDECL, [N.TYPE_DECL, T.IDENT, N.ARRAYSIZE]),
    26: Derivation(N.ARRAYSIZE, [T.OPEN_SB, T.INT_CONST, T.CLOSE_SB, N.ARRAYSIZE]),
    27: Derivation(N.ARRAYSIZE, []),
    28: Derivation(N.ATRIBSTAT, [N.LVALUE, T.ASSIGNMENT, N.ATRIBEXPR]),
    29: Derivation(N.ATRIBEXPR, [N.EXPRESSION]),
    30: Derivation(N.ATRIBEXPR, [N.ALLOCEXPRESSION]),
    31: Derivation(N.ATRIBEXPR, [N.FUNCCALL]),
    32: Derivation(N.FUNCCALL, [T.CALL, T.IDENT, T.OPEN_P, N.PARAMLISTCALL, T.CLOSE_P]),
    33: Derivation(N.PARAMLISTCALL, [T.IDENT, N.SOCALLMEMAYBE]),
    34: Derivation(N.PARAMLISTCALL, []),
    35: Derivation(N.SOCALLMEMAYBE, [T.COMMA, N.PARAMLISTCALL]),
    36: Derivation(N.SOCALLMEMAYBE, []),
    37: Derivation(N.PRINTSTAT, [T.PRINT, N.EXPRESSION]),
    38: Derivation(N.READSTAT, [T.READ, N.LVALUE]),
    39: Derivation(N.RETURNSTAT, [T.RETURN, N.EXPRESSION]),
    40: Derivation(
        N.IFSTAT,
        [
            T.IF,
            T.OPEN_P,
            N.EXPRESSION,
            T.CLOSE_P,
            T.OPEN_CB,
            N.STATELIST,
            T.CLOSE_CB,
            N.MAYBEELSE,
        ],
    ),
    41: Derivation(N.MAYBEELSE, [T.ELSE, T.OPEN_CB, N.STATELIST, T.CLOSE_CB]),
    42: Derivation(N.MAYBEELSE, []),
    43: Derivation(
        N.FORSTAT,
        [
            T.FOR,
            T.OPEN_P,
            N.ATRIBSTAT,
            T.SEMICOLON,
            N.EXPRESSION,
            T.SEMICOLON,
            N.ATRIBSTAT,
            T.CLOSE_P,
            N.STATEMENT,
        ],
    ),
    44: Derivation(N.STATELIST, [N.STATEMENT, N.MAYBESTATELIST]),
    45: Derivation(N.MAYBESTATELIST, [N.STATELIST]),
    46: Derivation(N.MAYBESTATELIST, []),
    47: Derivation(
        N.ALLOCEXPRESSION,
        [T.NEW, N.TYPE_DECL, T.OPEN_SB, N.NUMEXPRESSION, T.CLOSE_SB, N.INDEXEXPRESSION],
    ),
    48: Derivation(
        N.INDEXEXPRESSION, [T.OPEN_SB, N.NUMEXPRESSION, T.CLOSE_SB, N.INDEXEXPRESSION]
    ),
    49: Derivation(N.INDEXEXPRESSION, []),
    50: Derivation(
        N.EXPRESSION,
        [
            N.NUMEXPRESSION,
            semantic_actions_dict[2],
            N.MAYBECOMPARE,
            semantic_actions_dict[1],
        ],
    ),
    51: Derivation(
        N.MAYBECOMPARE,
        [
            N.COMPARISON,
            semantic_actions_dict[3],
            semantic_actions_dict[4],
            N.NUMEXPRESSION,
        ],
    ),
    52: Derivation(N.MAYBECOMPARE, [semantic_actions_dict[5]]),
    53: Derivation(N.COMPARISON, [T.LESS_THAN, semantic_actions_dict[6]]),
    54: Derivation(N.COMPARISON, [T.GREATER_THAN, semantic_actions_dict[6]]),
    55: Derivation(N.COMPARISON, [T.LESS_EQUAL, semantic_actions_dict[6]]),
    56: Derivation(N.COMPARISON, [T.GREATER_EQUAL, semantic_actions_dict[6]]),
    57: Derivation(N.COMPARISON, [T.EQUAL, semantic_actions_dict[6]]),
    58: Derivation(N.COMPARISON, [T.NOT_EQUAL, semantic_actions_dict[6]]),
    59: Derivation(
        N.NUMEXPRESSION,
        [N.TERM, semantic_actions_dict[2], N.INDEXTERM, semantic_actions_dict[1]],
    ),
    60: Derivation(
        N.INDEXTERM,
        [
            N.ADDSUB,
            N.TERM,
            semantic_actions_dict[8],
            N.INDEXTERM,
            semantic_actions_dict[7],
        ],
    ),
    61: Derivation(N.INDEXTERM, [semantic_actions_dict[5]]),
    62: Derivation(
        N.TERM,
        [N.UNARYEXPR, semantic_actions_dict[2], N.MULTUNARY, semantic_actions_dict[1]],
    ),
    63: Derivation(
        N.MULTUNARY,
        [
            N.MULDIV,
            N.UNARYEXPR,
            semantic_actions_dict[7],
            semantic_actions_dict[8],
            N.MULTUNARY,
        ],
    ),
    64: Derivation(N.MULTUNARY, [semantic_actions_dict[5]]),
    65: Derivation(N.MULDIV, [T.MULTIPLY]),
    66: Derivation(N.MULDIV, [T.DIVISION]),
    67: Derivation(N.MULDIV, [T.REMAINDER]),
    68: Derivation(N.MULDIV, [T.AND]),
    69: Derivation(N.ADDSUB, [T.ADDITION]),
    70: Derivation(N.ADDSUB, [T.SUBTRACT]),
    71: Derivation(N.ADDSUB, [T.OR]),
    72: Derivation(
        N.UNARYEXPR,
        [T.ADDITION, N.FACTOR, semantic_actions_dict[9], semantic_actions_dict[1]],
    ),
    73: Derivation(
        N.UNARYEXPR,
        [T.SUBTRACT, N.FACTOR, semantic_actions_dict[9], semantic_actions_dict[1]],
    ),
    74: Derivation(
        N.UNARYEXPR, [N.FACTOR, semantic_actions_dict[5], semantic_actions_dict[3]]
    ),
    75: Derivation(
        N.UNARYEXPR,
        [T.NOT, N.FACTOR, semantic_actions_dict[9], semantic_actions_dict[1]],
    ),
    76: Derivation(N.FACTOR, [T.INT_CONST, semantic_actions_dict[10]]),
    77: Derivation(N.FACTOR, [T.FLOAT_CONST, semantic_actions_dict[10]]),
    78: Derivation(N.FACTOR, [T.STRING_CONST]),
    79: Derivation(N.FACTOR, [T.NULL_CONST, semantic_actions_dict[10]]),
    80: Derivation(N.FACTOR, [N.LVALUE, semantic_actions_dict[11]]),
    81: Derivation(
        N.FACTOR, [T.OPEN_P, N.EXPRESSION, T.CLOSE_P, semantic_actions_dict[12]]
    ),
    82: Derivation(N.LVALUE, [T.IDENT, semantic_actions_dict[10], N.INDEXEXPRESSION]),
}

DerivationTable = {
    N.PROGRAM: {
        T.DEF: 2,
        T.IDENT: 1,
        T.OPEN_CB: 1,
        T.INT: 1,
        T.FLOAT: 1,
        T.STRING: 1,
        T.SEMICOLON: 1,
        T.BREAK: 1,
        T.PRINT: 1,
        T.READ: 1,
        T.RETURN: 1,
        T.IF: 1,
        T.FOR: 1,
        "": 3,
    },
    N.FUNCLIST: {T.DEF: 4},
    N.MOREFUNCS: {T.DEF: 5, "": 6},
    N.FUNCDEF: {T.DEF: 7},
    N.PARAMLIST: {T.INT: 8, T.FLOAT: 8, T.STRING: 8},
    N.PARAMETER: {T.IDENT: 9},
    N.MAYBEPARAMS: {T.CLOSE_P: 11, T.COMMA: 10},
    N.TYPE_DECL: {T.INT: 12, T.FLOAT: 13, T.STRING: 14},
    N.STATEMENT: {
        T.IDENT: 16,
        T.OPEN_CB: 22,
        T.INT: 15,
        T.FLOAT: 15,
        T.STRING: 15,
        T.SEMICOLON: 24,
        T.BREAK: 23,
        T.PRINT: 17,
        T.READ: 18,
        T.RETURN: 19,
        T.IF: 20,
        T.FOR: 21,
    },
    N.VARDECL: {T.INT: 25, T.FLOAT: 25, T.STRING: 25},
    N.ARRAYSIZE: {T.SEMICOLON: 27, T.OPEN_SB: 26},
    N.ATRIBSTAT: {T.IDENT: 28},
    N.ATRIBEXPR: {
        T.IDENT: 29,
        T.OPEN_P: 29,
        T.INT_CONST: 29,
        T.CALL: 31,
        T.NEW: 30,
        T.ADDITION: 29,
        T.SUBTRACT: 29,
        T.NOT: 29,
        T.FLOAT_CONST: 29,
        T.STRING_CONST: 29,
        T.NULL_CONST: 29,
    },
    N.FUNCCALL: {T.CALL: 32},
    N.PARAMLISTCALL: {T.IDENT: 33, T.CLOSE_P: 34},
    N.SOCALLMEMAYBE: {T.CLOSE_P: 36, T.COMMA: 35},
    N.PRINTSTAT: {T.PRINT: 37},
    N.READSTAT: {T.READ: 38},
    N.RETURNSTAT: {T.RETURN: 39},
    N.IFSTAT: {T.IF: 40},
    N.MAYBEELSE: {
        T.IDENT: 42,
        T.OPEN_CB: 42,
        T.CLOSE_CB: 42,
        T.INT: 42,
        T.FLOAT: 42,
        T.STRING: 42,
        T.SEMICOLON: 42,
        T.BREAK: 42,
        T.PRINT: 42,
        T.READ: 42,
        T.RETURN: 42,
        T.IF: 42,
        T.ELSE: 41,
        T.FOR: 42,
        "": 42,
    },
    N.FORSTAT: {T.FOR: 43},
    N.STATELIST: {
        T.IDENT: 44,
        T.OPEN_CB: 44,
        T.INT: 44,
        T.FLOAT: 44,
        T.STRING: 44,
        T.SEMICOLON: 44,
        T.BREAK: 44,
        T.PRINT: 44,
        T.READ: 44,
        T.RETURN: 44,
        T.IF: 44,
        T.FOR: 44,
    },
    N.MAYBESTATELIST: {
        T.IDENT: 45,
        T.OPEN_CB: 45,
        T.CLOSE_CB: 46,
        T.INT: 45,
        T.FLOAT: 45,
        T.STRING: 45,
        T.SEMICOLON: 45,
        T.BREAK: 45,
        T.PRINT: 45,
        T.READ: 45,
        T.RETURN: 45,
        T.IF: 45,
        T.FOR: 45,
    },
    N.ALLOCEXPRESSION: {T.NEW: 47},
    N.INDEXEXPRESSION: {
        T.CLOSE_P: 49,
        T.SEMICOLON: 49,
        T.OPEN_SB: 48,
        T.CLOSE_SB: 49,
        T.ASSIGNMENT: 49,
        T.LESS_THAN: 49,
        T.GREATER_THAN: 49,
        T.LESS_EQUAL: 49,
        T.GREATER_EQUAL: 49,
        T.EQUAL: 49,
        T.NOT_EQUAL: 49,
        T.MULTIPLY: 49,
        T.DIVISION: 49,
        T.REMAINDER: 49,
        T.AND: 49,
        T.ADDITION: 49,
        T.SUBTRACT: 49,
        T.OR: 49,
    },
    N.EXPRESSION: {
        T.IDENT: 50,
        T.OPEN_P: 50,
        T.INT_CONST: 50,
        T.ADDITION: 50,
        T.SUBTRACT: 50,
        T.NOT: 50,
        T.FLOAT_CONST: 50,
        T.STRING_CONST: 50,
        T.NULL_CONST: 50,
    },
    N.MAYBECOMPARE: {
        T.CLOSE_P: 52,
        T.SEMICOLON: 52,
        T.LESS_THAN: 51,
        T.GREATER_THAN: 51,
        T.LESS_EQUAL: 51,
        T.GREATER_EQUAL: 51,
        T.EQUAL: 51,
        T.NOT_EQUAL: 51,
    },
    N.COMPARISON: {
        T.LESS_THAN: 53,
        T.GREATER_THAN: 54,
        T.LESS_EQUAL: 55,
        T.GREATER_EQUAL: 56,
        T.EQUAL: 57,
        T.NOT_EQUAL: 58,
    },
    N.NUMEXPRESSION: {
        T.IDENT: 59,
        T.OPEN_P: 59,
        T.INT_CONST: 59,
        T.ADDITION: 59,
        T.SUBTRACT: 59,
        T.NOT: 59,
        T.FLOAT_CONST: 59,
        T.STRING_CONST: 59,
        T.NULL_CONST: 59,
    },
    N.INDEXTERM: {
        T.CLOSE_P: 61,
        T.SEMICOLON: 61,
        T.CLOSE_SB: 61,
        T.LESS_THAN: 61,
        T.GREATER_THAN: 61,
        T.LESS_EQUAL: 61,
        T.GREATER_EQUAL: 61,
        T.EQUAL: 61,
        T.NOT_EQUAL: 61,
        T.ADDITION: 60,
        T.SUBTRACT: 60,
        T.OR: 60,
    },
    N.TERM: {
        T.IDENT: 62,
        T.OPEN_P: 62,
        T.INT_CONST: 62,
        T.ADDITION: 62,
        T.SUBTRACT: 62,
        T.NOT: 62,
        T.FLOAT_CONST: 62,
        T.STRING_CONST: 62,
        T.NULL_CONST: 62,
    },
    N.MULTUNARY: {
        T.CLOSE_P: 64,
        T.SEMICOLON: 64,
        T.CLOSE_SB: 64,
        T.LESS_THAN: 64,
        T.GREATER_THAN: 64,
        T.LESS_EQUAL: 64,
        T.GREATER_EQUAL: 64,
        T.EQUAL: 64,
        T.NOT_EQUAL: 64,
        T.MULTIPLY: 63,
        T.DIVISION: 63,
        T.REMAINDER: 63,
        T.AND: 63,
        T.ADDITION: 64,
        T.SUBTRACT: 64,
        T.OR: 64,
    },
    N.MULDIV: {T.MULTIPLY: 65, T.DIVISION: 66, T.REMAINDER: 67, T.AND: 68},
    N.ADDSUB: {T.ADDITION: 69, T.SUBTRACT: 70, T.OR: 71},
    N.UNARYEXPR: {
        T.IDENT: 74,
        T.OPEN_P: 74,
        T.INT_CONST: 74,
        T.ADDITION: 72,
        T.SUBTRACT: 73,
        T.NOT: 75,
        T.FLOAT_CONST: 74,
        T.STRING_CONST: 74,
        T.NULL_CONST: 74,
    },
    N.FACTOR: {
        T.IDENT: 80,
        T.OPEN_P: 81,
        T.INT_CONST: 76,
        T.FLOAT_CONST: 77,
        T.STRING_CONST: 78,
        T.NULL_CONST: 79,
    },
    N.LVALUE: {T.IDENT: 82},
}
