#ifndef GRAMMAR_SYMBOLS_H
#define GRAMMAR_SYMBOLS_H

enum Terminal {
    IDENT,
    OPEN_P,         // (
    CLOSE_P,        // )
    OPEN_SB,        // [
    CLOSE_SB,       // ]
    OPEN_CB,        // {
    CLOSE_CB,       // }
    COMMA,          // ,
    SEMICOLON,      // ;
    MULTIPLY,       // *
    DIVISION,       // /
    REMAINDER,      // %
    ADDITION,       // +
    SUBTRACT,       // -
    ASSIGNMENT,     // =
    LESS_THAN,      // <
    GREATER_THAN,   // >
    LESS_EQUAL,     // <=
    GREATER_EQUAL,  // >=
    EQUAL,          // ==
    NOT_EQUAL,      // !=
    DEF,
    NEW,
    INT,
    FLOAT,
    STRING,
    PRINT,
    READ,
    RETURN,
    BREAK,
    IF,
    ELSE,
    FOR,
    INT_CONST,
    FLOAT_CONST,
    STRING_CONST,
    NULL_CONST,  // null
    AND,
    OR,
    NOT,
    CALL
};

enum NonTerminal {
    PROGRAM,
    FUNCLIST,
    MOREFUNCS,
    FUNCDEF,
    PARAMLIST,
    PARAMETER,
    MAYBEPARAMS,
    TYPE_DECL,  // type
    STATEMENT,
    VARDECL,
    ARRAYSIZE,
    ATRIBSTAT,
    ATRIBEXPR,
    FUNCCALL,
    PARAMLISTCALL,
    SOCALLMEMAYBE,
    PRINTSTAT,
    READSTAT,
    RETURNSTAT,
    IFSTAT,
    MAYBEELSE,
    FORSTAT,
    STATELIST,
    MAYBESTATELIST,
    ALLOCEXPRESSION,
    INDEXEXPRESSION,
    EXPRESSION,
    MAYBECOMPARE,
    COMPARISON,
    NUMEXPRESSION,
    INDEXTERM,
    TERM,
    MULTUNARY,
    MULDIV,
    ADDSUB,
    UNARYEXPR,
    FACTOR,
    LVALUE
};

#endif