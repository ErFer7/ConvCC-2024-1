#include <list>
#include <string>
#include <unordered_map>

#include "data/error_codes.h"
#include "data/symbol_table.h"

int lexical_analyser(std::string source,
                     std::list<int> &token_list,
                     std::unordered_map<std::string, std::list<unsigned int>> &symbol_table);