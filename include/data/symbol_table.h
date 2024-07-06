#pragma once

#include <list>
#include <string>
#include <unordered_map>

class SymbolTable {
   public:
    void add_instance(std::string token, unsigned int line);
    std::list<unsigned int> get_instances(std::string token);

   private:
    std::unordered_map<std::string, std::list<unsigned int>> token_map;
    // add value as attribute
};
