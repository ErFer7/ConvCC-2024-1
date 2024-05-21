#include <unordered_map>
#include <string>
#include <list>
#include "data/symbol_table.h"
#include "data/error_codes.h"

enum Terminals {
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
    DIVIDE,         // /
    REMAINDER,      // %
    ADD,            // +
    SUB,            // -
    ASSIGN,         // =
    LESS,           // <
    GREATER,        // >
    LESS_EQUAL,     // <=
    GREATER_EQUAL,  // >=
    EQUAL,          // ==
    NOT_EQUAL,      // !=
    DEF,            // def
    NEW,            // new
    INT,            // int
    FLOAT,          // float
    STRING,         // string
    PRINT,          // print
    READ,           // read
    RETURN,         // return
    BREAK,          // break
    IF,             // if
    ELSE,           // else
    FOR,            // for
    INT_CONSTANT,   
    FLOAT_CONSTANT, 
    STRING_CONSTANT,
    NULL_CONSTANT   //null
};

std::unordered_map<std::string,Terminals> Tokens = {
    {"(",OPEN_P},{")",CLOSE_P},{"[",OPEN_SB},{"]",CLOSE_SB},
    {"{",OPEN_CB},{"}",CLOSE_CB},{",",COMMA},{";",SEMICOLON},
    {"=",ASSIGN},{"<",LESS},{">",GREATER},{"<=",LESS_EQUAL},
    {">=",GREATER_EQUAL},{"==",EQUAL},{"!=",NOT_EQUAL},{"*",MULTIPLY},
    {"/",DIVIDE},{"%",REMAINDER},{"+",ADD},{"-",SUB},
    {"def",DEF},{"new",NEW},{"int",INT},{"float",FLOAT},
    {"string",STRING},{"print",PRINT},{"read",READ},{"return",RETURN},
    {"break",BREAK},{"if",IF},{"else",ELSE},{"for",FOR},
    {"null",NULL_CONSTANT}
};

enum TokenRecognizerStates {
    READ_SIMPLE,        // skips whitespace,catches 1-char tokens,sends to other states
    MAYBE_IDENT,        // reads a word, then checks if it's a keyword
    NUMERAL,            // starts in a digit, may be int or float
    FLOAT_FRACTIONAL,   // fractional portion of float
    STRING_LITERAL,     // looks for string termination
    COMPARE_ASSIGN,     // may find = or ==, < or <=, > or >=
    DIFFERENT           // must find = after !
};

int lexical_analyser(std::string source) {
    unsigned int
        state = READ_SIMPLE, 
        token_start_pos = 0, // should somehow be used to handle error messages, error at pos n
        current_pos = 0,
        size = source.size();
    char next;
    std::string current_token;
    while (current_pos < size) {
        next = source[current_pos];
        switch (state)
        {
        case READ_SIMPLE:
            if (isspace(next)) {
                current_pos++;
                break;
            } else if (isalpha(next) || next == '_') {  // start of ident or keyword
                state = MAYBE_IDENT;
                token_start_pos = current_pos;
                current_token += next;
            } else if (isdigit(next)) {                 // start of number
                state = NUMERAL;
                token_start_pos = current_pos;
            } else if (next == '\"') {                  // start of string
                state = STRING_LITERAL;
                token_start_pos = current_pos;
            } else if (next == '=' || next == '>' || next == '<') {
                state == COMPARE_ASSIGN;
                current_token += next;
            } else if (next == '!') {
                state == DIFFERENT;
                token_start_pos = current_pos;
            } else if (Tokens[std::string(1,next)] < ASSIGN) { // if token is 1-char and not <>= because those can be start of others
                TokenList.push_back(Tokens[std::string(1,next)]);
            } else {
                token_start_pos = current_pos;
                return INVALID_CHAR; // error: invalid character in position {token_start_pos}
            }
            current_pos++;
            break;
        case MAYBE_IDENT:
            if (isalnum(next) || next == '_') {
                current_token += next;
                current_pos++;
            } else {
                state = READ_SIMPLE;
                if (Tokens.find(current_token) != Tokens.end()) { // is keyword
                    TokenList.push_back(Tokens[current_token]);
                } else if (SymbolTable.find(current_token) == SymbolTable.end()) { // not in symbol table
                    SymbolTable[current_token] = {current_pos};
                    TokenList.push_back(IDENT);
                } else { // already in symbol table
                    SymbolTable[current_token].push_back(current_pos);
                    TokenList.push_back(IDENT);
                }
                current_token.clear();
            }
            break;
        case NUMERAL:
            if (isdigit(next)) {
                current_pos++;
            } else if (next == '.') {
                state = FLOAT_FRACTIONAL;
                current_pos++;
            } else if (isalpha(next) || next == '_') {
                return INVALID_NUMBER_FORMAT;
            } else {
                state = READ_SIMPLE;
                TokenList.push_back(INT_CONSTANT);
            }
            break;
        case FLOAT_FRACTIONAL:
            if (isdigit(next)) {
                current_pos++;
            } else if (isalpha(next) || next == '_') {
                return INVALID_NUMBER_FORMAT;
            } else {
                state = READ_SIMPLE;
                TokenList.push_back(FLOAT_CONSTANT);
            }
            break;
        case STRING_LITERAL: // does not handle escaping characters
            if (next == '\"') {
                state == READ_SIMPLE;
                TokenList.push_back(STRING_CONSTANT);
            }
            current_pos++;
            break;
        case COMPARE_ASSIGN:
            if (next == '=') {
                current_token += next;
                current_pos++;
            }
            state = READ_SIMPLE;
            TokenList.push_back(Tokens[current_token]);
            current_token.clear();
            break;
        case DIFFERENT:
            if (next == '=') {
                current_token += next;
                current_pos++;
                state = READ_SIMPLE;
                TokenList.push_back(NOT_EQUAL);
                current_token.clear();
            } else return INVALID_CHAR; // error: invalid '!' in position {token_start_pos}
            break;
        default:
            printf("what"); // what
            break;
        }
    }
    return LEX_OK;
}