#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

#include "lexical_analyzer.h"
#include "data/symbol_table.h"
#include "data/token_list.h"


int main(int argc, char **argv) {
    if (argc < 2) return 1;
    std::ifstream sourcefile (argv[1]);
    if (!sourcefile.is_open()) return 1;
    std::ostringstream sourcestream;
    sourcestream << sourcefile.rdbuf();
    std::string sourcestring = sourcestream.str();

    TokenList token_list = TokenList();
    SymbolTable symbol_table = SymbolTable();

    int result = lexical_analyser(sourcestring,token_list,symbol_table);

    printf("%s\n",sourcestring.c_str());
    while (!token_list.empty()){
        printf("%d ",token_list.pop_front().type);
    }
    printf("\n");

    return 0;
}