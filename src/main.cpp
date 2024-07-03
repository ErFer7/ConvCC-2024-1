// Compilador para a linguagem Jegb

#include <array>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include "data/symbol_table.h"
#include "data/token_list.h"
#include "enums/return_codes.h"
#include "lexical_analyzer.h"

std::array<std::string, 41> token_to_name = {
    "ident", "(",      ")",     "[",   "]",    "{",   "}",         ",",           ";",
    "*",     "/",      "%",     "+",   "-",    "=",   "<",         ">",           "<=",
    ">=",    "==",     "!=",    "def", "new",  "int", "float",     "string",      "print",
    "read",  "return", "break", "if",  "else", "for", "int_const", "float_const", "string_const",
    "null",  "and",    "or",    "not", "call"};

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cout << "Usage: lexical_test \"source_file.txt\"" << std::endl;
        return 1;
    }

    std::ifstream sourcefile(argv[1]);

    if (!sourcefile.is_open())
        return 1;

    std::ostringstream sourcestream;
    sourcestream << sourcefile.rdbuf();
    std::string sourcestring = sourcestream.str();

    TokenList token_list = TokenList();
    SymbolTable symbol_table = SymbolTable();

    LexicalReturnCode return_code = LexicalAnalyzer::analyze(sourcestring, token_list, symbol_table);

    std::cout << "Status: " << return_code << std::endl;
    std::cout << "Token list contents: " << std::endl;

    while (!token_list.empty()) {
        Token token = token_list.pop_front();
        std::cout << "<" << token_to_name[token.type] << ", " << token.data << "> ";
    }

    return 0;
}