#include "lexical_analyzer.h"

#include <cctype>
#include <string>
#include <unordered_map>

#include "data/symbol_table.h"
#include "data/token_list.h"
#include "enums/grammar_symbols.h"

const std::unordered_map<std::string, Terminal> LexicalAnalyzer::_TOKEN_STRINGS = {
    {"(", OPEN_P},       {")", CLOSE_P},      {"[", OPEN_SB},        {"]", CLOSE_SB},   {"{", OPEN_CB},
    {"}", CLOSE_CB},     {",", COMMA},        {";", SEMICOLON},      {"=", ASSIGNMENT}, {"<", LESS_THAN},
    {">", GREATER_THAN}, {"<=", LESS_EQUAL},  {">=", GREATER_EQUAL}, {"==", EQUAL},     {"!=", NOT_EQUAL},
    {"*", MULTIPLY},     {"/", DIVISION},     {"%", REMAINDER},      {"+", ADDITION},   {"-", SUBTRACT},
    {"def", DEF},        {"new", NEW},        {"int", INT},          {"float", FLOAT},  {"string", STRING},
    {"print", PRINT},    {"read", READ},      {"return", RETURN},    {"break", BREAK},  {"if", IF},
    {"else", ELSE},      {"for", FOR},        {"and", AND},          {"or", OR},        {"not", NOT},
    {"call", CALL},      {"null", NULL_CONST}};

Terminal LexicalAnalyzer::check_identifier(unsigned int current_line,
                                           std::string current_token,
                                           SymbolTable &symbol_table) {
    // Checks if token is a keyword.
    // If so, returns corresponding kw;
    // Otherwise adds it to symbol table if not already in it, returning IDENT.
    if (_TOKEN_STRINGS.find(current_token) != _TOKEN_STRINGS.end())
        return _TOKEN_STRINGS.at(current_token);
    symbol_table.add_instance(current_token, current_line);
    return IDENT;
};

LexicalReturnCode LexicalAnalyzer::analyze(std::string source, TokenList &token_list, SymbolTable &symbol_table) {
    TokenParserStates state = WHITE_SPACE;
    unsigned int current_line = 1, current_column = 1, token_column = 1, current_pos = 0, size = source.size();
    char next;
    std::string current_token;

    while (current_pos < size) {
        next = source[current_pos];
        switch (state) {
            case WHITE_SPACE:
                if (isspace(next)) {
                    if (next == '\n') {
                        current_line++;
                        current_column = 0;
                    }
                    current_pos++;
                    current_column++;
                } else {
                    state = READ_SIMPLE;
                }
                break;
            case READ_SIMPLE:
                token_column = current_column;
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
                    // if token is 1-char and not < | > | =
                } else {
                    std::string key = std::string(1, next);

                    if (_TOKEN_STRINGS.find(key) != _TOKEN_STRINGS.end() && _TOKEN_STRINGS.at(key) < ASSIGNMENT) {
                        Terminal current_symbol = _TOKEN_STRINGS.at(key);
                        token_list.push_back(current_symbol, current_line, token_column);
                        state = WHITE_SPACE;
                    } else {
                        return INVALID_CHAR;  // error: invalid character in line N
                    }
                }
                current_pos++;
                current_column++;
                break;
            case MAYBE_IDENT:
                if (isalnum(next) || next == '_') {
                    current_token += next;
                    current_pos++;
                    current_column++;
                } else {
                    state = WHITE_SPACE;
                    Terminal result = check_identifier(current_line, current_token, symbol_table);
                    std::string data = result == IDENT ? current_token : "";
                    token_list.push_back(result, current_line, token_column, data);
                    current_token.clear();
                }
                break;
            case NUMERAL:
                if (isdigit(next)) {
                    current_token += next;
                    current_pos++;
                    current_column++;
                } else if (next == '.') {
                    state = FLOAT_FRACTIONAL;
                    current_token += next;
                    current_pos++;
                    current_column++;
                } else if (isalpha(next) || next == '_') {
                    return INVALID_NUMBER_FORMAT;
                } else {
                    state = WHITE_SPACE;
                    token_list.push_back(INT_CONST, current_line, token_column, current_token);
                    current_token.clear();
                }
                break;
            case FLOAT_FRACTIONAL:
                if (isdigit(next)) {
                    current_token += next;
                    current_pos++;
                    current_column++;
                } else if (isalpha(next) || next == '_') {
                    return INVALID_NUMBER_FORMAT;
                } else {
                    state = WHITE_SPACE;
                    token_list.push_back(FLOAT_CONST, current_line, token_column, current_token);
                    current_token.clear();
                }
                break;
            case STRING_LITERAL:  // You can't escape! (it doesnt escape chars)
                if (next == '\"') {
                    state = WHITE_SPACE;
                    token_list.push_back(STRING_CONST, current_line, token_column, current_token);
                    current_token.clear();
                } else if (next == '\n') {  // no multiline strings
                    return UNCLOSED_STRING;
                } else {
                    current_token += next;
                }
                current_pos++;
                current_column++;
                break;
            case ASSIGN_OR_EQUAL:
                if (next == '=') {
                    token_list.push_back(EQUAL, current_line, token_column);
                    current_pos++;
                    current_column++;
                } else {
                    token_list.push_back(ASSIGNMENT, current_line, token_column);
                }
                state = WHITE_SPACE;
                break;
            case GREATER_OR_GE:
                if (next == '=') {
                    token_list.push_back(GREATER_EQUAL, current_line, token_column);
                    current_pos++;
                    current_column++;
                } else {
                    token_list.push_back(GREATER_THAN, current_line, token_column);
                }
                state = WHITE_SPACE;
                break;
            case LESS_OR_LE:
                if (next == '=') {
                    token_list.push_back(LESS_EQUAL, current_line, token_column);
                    current_pos++;
                    current_column++;
                } else {
                    token_list.push_back(LESS_THAN, current_line, token_column);
                }
                state = WHITE_SPACE;
                break;
            case DIFFERENT:
                if (next == '=') {
                    current_token += next;
                    current_pos++;
                    current_column++;
                    state = WHITE_SPACE;
                    token_list.push_back(NOT_EQUAL, current_line, token_column);
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