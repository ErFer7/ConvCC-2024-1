#include <list>
#include <string>
#include <unordered_map>

#include "data/error_codes.h"
#include "data/grammar_symbols.h"
#include "data/symbol_table.h"
#include "data/token_list.h"

std::unordered_map<std::string, Symbols> TokenStrings = {
    {"(", OPEN_P},       {")", CLOSE_P},      {"[", OPEN_SB},        {"]", CLOSE_SB},   {"{", OPEN_CB},
    {"}", CLOSE_CB},     {",", COMMA},        {";", SEMICOLON},      {"=", ASSIGNMENT}, {"<", LESS_THAN},
    {">", GREATER_THAN}, {"<=", LESS_EQUAL},  {">=", GREATER_EQUAL}, {"==", EQUAL},     {"!=", NOT_EQUAL},
    {"*", MULTIPLY},     {"/", DIVISION},     {"%", REMAINDER},      {"+", ADDITION},   {"-", SUBTRACT},
    {"def", DEF},        {"new", NEW},        {"int", INT},          {"float", FLOAT},  {"string", STRING},
    {"print", PRINT},    {"read", READ},      {"return", RETURN},    {"break", BREAK},  {"if", IF},
    {"else", ELSE},      {"for", FOR},        {"and", AND},          {"or", OR},        {"not", NOT},
    {"call", CALL},      {"null", NULL_CONST}};

enum TokenParserStates {
    WHITE_SPACE,       // You have been living here for as long as you can remember
    READ_SIMPLE,       // catches 1-char tokens,sends to other states
    MAYBE_IDENT,       // reads a word, then checks if it's a keyword
    NUMERAL,           // starts in a digit, may be int or float
    FLOAT_FRACTIONAL,  // fractional portion of float
    STRING_LITERAL,    // looks for string termination
    ASSIGN_OR_EQUAL,   // may find = or ==
    GREATER_OR_GE,     // may find > or >=
    LESS_OR_LE,        // may find < or <=
    DIFFERENT          // must find = after !
};

Symbols check_ident(unsigned int current_line,
                std::string current_token,
                SymbolTable &symbol_table) {
    // Checks if token is a keyword.
    // If so, returns corresponding kw;
    // Otherwise adds it to symbol table if not already in it, returning IDENT.
    if (TokenStrings.find(current_token) != TokenStrings.end())
        return TokenStrings[current_token];
    symbol_table.add_instance(current_token,current_line);
    return IDENT;
};

int lexical_analyser(std::string source,
                     TokenList &token_list,
                     SymbolTable &symbol_table) {
    unsigned int state = WHITE_SPACE, current_line = 1, current_pos = 0, size = source.size();
    char next;
    std::string current_token;
    while (current_pos < size) {
        next = source[current_pos];
        switch (state) {
            case WHITE_SPACE:
                if (isspace(next)) {
                    if (next == '\n') current_line++;
                    current_pos++;
                } else {
                    state = READ_SIMPLE;
                }
                break;
            case READ_SIMPLE:
                if (isalpha(next) || next == '_') {  // start of ident or keyword
                    state = MAYBE_IDENT;
                    current_token += next;
                } else if (isdigit(next)) {  // start of number
                    state = NUMERAL;
                    current_token += next;
                } else if (next == '\"') {  // start of string
                    state = STRING_LITERAL;
                } else if (next == '=') {
                    state = ASSIGN_OR_EQUAL;
                } else if (next == '>') {
                    state = GREATER_OR_GE;
                } else if (next == '<') {
                    state = LESS_OR_LE;
                } else if (next == '!') {
                    state = DIFFERENT;
                } else if (TokenStrings[std::string(1, next)] < ASSIGNMENT) {  // if token is 1-char and not < | > | =
                    Symbols cur_symbol = TokenStrings[std::string(1, next)];
                    token_list.push_back(cur_symbol);
                    state = WHITE_SPACE;
                } else {
                    return INVALID_CHAR;  // error: invalid character in line N
                }
                current_pos++;
                break;
            case MAYBE_IDENT:
                if (isalnum(next) || next == '_') {
                    current_token += next;
                    current_pos++;
                } else {
                    state = WHITE_SPACE;
                    Symbols result = check_ident(current_line, current_token, symbol_table);
                    token_list.push_back(result,result==IDENT?current_token:"");
                    current_token.clear();
                }
                break;
            case NUMERAL:
                if (isdigit(next)) {
                    current_token += next;
                    current_pos++;
                } else if (next == '.') {
                    state = FLOAT_FRACTIONAL;
                    current_token += next;
                    current_pos++;
                } else if (isalpha(next) || next == '_') {
                    return INVALID_NUMBER_FORMAT;
                } else {
                    state = WHITE_SPACE;
                    token_list.push_back(INT_CONST,current_token);
                    current_token.clear();
                }
                break;
            case FLOAT_FRACTIONAL:
                if (isdigit(next)) {
                    current_token += next;
                    current_pos++;
                } else if (isalpha(next) || next == '_') {
                    return INVALID_NUMBER_FORMAT;
                } else {
                    state = WHITE_SPACE;
                    token_list.push_back(FLOAT_CONST,current_token);
                    current_token.clear();
                }
                break;
            case STRING_LITERAL:  // You can't escape! (it doesnt escape chars)
                if (next == '\"') {
                    state == WHITE_SPACE;
                    token_list.push_back(STRING_CONST,current_token);
                    current_token.clear();
                } else if (next == '\n') {  // no multiline strings
                    return UNCLOSED_STRING;
                }
                current_token += next;
                current_pos++;
                break;
            case ASSIGN_OR_EQUAL:
                if (next == '=') {
                    token_list.push_back(EQUAL);
                    current_pos++;
                } else {
                    token_list.push_back(ASSIGNMENT);
                }
                state = WHITE_SPACE;
                break;
            case GREATER_OR_GE:
                if (next == '=') {
                    token_list.push_back(GREATER_EQUAL);
                    current_pos++;
                } else {
                    token_list.push_back(GREATER_THAN);
                }
                state = WHITE_SPACE;
                break;
            case LESS_OR_LE:
                if (next == '=') {
                    token_list.push_back(LESS_EQUAL);
                    current_pos++;
                } else {
                    token_list.push_back(LESS_THAN);
                }
                state = WHITE_SPACE;
                break;
            case DIFFERENT:
                if (next == '=') {
                    current_token += next;
                    current_pos++;
                    state = WHITE_SPACE;
                    token_list.push_back(NOT_EQUAL);
                    current_token.clear();
                } else
                    return INVALID_CHAR;  // error: invalid '!' in line N
                break;
            default:
                printf("\n\nwhat\n\n");  // GREED /// THIRD : A SHOT IN THE DARK
                break;
        }
    }
    return LEX_OK;
}