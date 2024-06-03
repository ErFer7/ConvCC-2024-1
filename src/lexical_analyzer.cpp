#include <list>
#include <string>
#include <unordered_map>

#include "data/error_codes.h"
#include "data/symbol_table.h"

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
    READ_SIMPLE,       // skips whitespace,catches 1-char tokens,sends to other states
    MAYBE_IDENT,       // reads a word, then checks if it's a keyword
    NUMERAL,           // starts in a digit, may be int or float
    FLOAT_FRACTIONAL,  // fractional portion of float
    STRING_LITERAL,    // looks for string termination
    COMPARE_ASSIGN,    // may find = or ==, < or <=, > or >=
    DIFFERENT          // must find = after !
};

int lexical_analyser(std::string source,
                     std::list<int> &token_list,
                     std::unordered_map<std::string, std::list<unsigned int>> &symbol_table) {
    unsigned int state = READ_SIMPLE, current_line = 1, current_pos = 0, size = source.size();
    char next;
    std::string current_token;
    while (current_pos < size) {
        next = source[current_pos];
        switch (state) {
            case READ_SIMPLE:
                if (isspace(next)) {
                    if (next == '\n') current_line++;
                    current_pos++;
                    break;
                } else if (isalpha(next) || next == '_') {  // start of ident or keyword
                    state = MAYBE_IDENT;
                    current_token += next;
                } else if (isdigit(next)) {  // start of number
                    state = NUMERAL;
                } else if (next == '\"') {  // start of string
                    state = STRING_LITERAL;
                } else if (next == '=' || next == '>' || next == '<') {
                    state = COMPARE_ASSIGN;
                    current_token += next;
                } else if (next == '!') {
                    state = DIFFERENT;
                } else if (TokenStrings[std::string(1, next)] < ASSIGNMENT) {  // if token is 1-char and not < | > | =
                    token_list.push_back(TokenStrings[std::string(1, next)]);
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
                    state = READ_SIMPLE;
                    if (TokenStrings.find(current_token) != TokenStrings.end()) {  // is keyword
                        token_list.push_back(TokenStrings[current_token]);
                    } else if (symbol_table.find(current_token) == symbol_table.end()) {  // not in table
                        symbol_table[current_token] = {current_pos};
                        token_list.push_back(IDENT);
                    } else {  // already in table
                        symbol_table[current_token].push_back(current_pos);
                        token_list.push_back(IDENT);
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
                    token_list.push_back(INT_CONST);
                }
                break;
            case FLOAT_FRACTIONAL:
                if (isdigit(next)) {
                    current_pos++;
                } else if (isalpha(next) || next == '_') {
                    return INVALID_NUMBER_FORMAT;
                } else {
                    state = READ_SIMPLE;
                    token_list.push_back(FLOAT_CONST);
                }
                break;
            case STRING_LITERAL:  // You can't escape! (it doesnt escape chars)
                if (next == '\"') {
                    state == READ_SIMPLE;
                    token_list.push_back(STRING_CONST);
                }
                current_pos++;
                break;
            case COMPARE_ASSIGN:
                if (next == '=') {
                    current_token += next;
                    current_pos++;
                }
                state = READ_SIMPLE;
                token_list.push_back(TokenStrings[current_token]);
                current_token.clear();
                break;
            case DIFFERENT:
                if (next == '=') {
                    current_token += next;
                    current_pos++;
                    state = READ_SIMPLE;
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