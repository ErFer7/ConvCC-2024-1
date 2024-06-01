#include <list>
#include <string>
#include <unordered_map>

std::unordered_map<std::string, std::list<unsigned int>> SymbolTable;

std::list<int> TokenList;

enum Symbols {
    /// TERMINALS ///
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
    /// TODO: INSERT NON-TERMINALS AFTER THIS POINT FOR SYNTAX ANALYSIS///
};