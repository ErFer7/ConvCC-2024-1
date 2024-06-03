#include <list>
#include <string>
#include <unordered_map>

int lexical_analyser(std::string source,
                     std::list<int> &token_list,
                     std::unordered_map<std::string, std::list<unsigned int>> &symbol_table);