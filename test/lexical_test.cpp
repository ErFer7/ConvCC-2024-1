#include <fstream>
#include <iostream>
#include <array>
#include <sstream>
#include <string>

#include "data/symbol_table.h"
#include "data/token_list.h"
#include "lexical_analyzer.h"

std::array<std::string,41> token_to_name = {
    "ident", "(",      ")",     "[",   "]",    "{",   "}",         ",",           ";",
    "*",     "/",      "%",     "+",   "-",    "=",   "<",         ">",           "<=",
    ">=",    "==",     "!=",    "def", "new",  "int", "float",     "string",      "print",
    "read",  "return", "break", "if",  "else", "for", "int_const", "float_const", "string_const",
    "null",  "and",    "or",    "not", "call"};

int main(int argc, char **argv) {
    /*
    Reads a source file in the ConvCC language and parses it,
    prints back the sequence of tokens that were read.

    Variable/function names, numbers, strings are simply
    identified as their type, ignoring their value.
    */

    if (argc < 2) {
        printf("Usage: lexical_test \"source_file.txt\"");
        return 1;
    }
    std::ifstream sourcefile(argv[1]);
    if (!sourcefile.is_open()) return 1;
    std::ostringstream sourcestream;
    sourcestream << sourcefile.rdbuf();
    std::string sourcestring = sourcestream.str();

    TokenList token_list = TokenList();
    SymbolTable symbol_table = SymbolTable();

    int result = lexical_analyser(sourcestring, token_list, symbol_table);

    printf("%s\n", sourcestring.c_str());
    while (!token_list.empty()) {
        printf("%s ", token_to_name[int(token_list.pop_front().type)].c_str());
    }
    printf("\n");

    return 0;
}