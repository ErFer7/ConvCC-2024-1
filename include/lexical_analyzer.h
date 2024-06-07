#include <list>
#include <string>
#include <unordered_map>
#include "data/token_list.h"
#include "data/symbol_table.h"

int lexical_analyser(std::string source,
                     TokenList &token_list,
                     SymbolTable &symbol_table);