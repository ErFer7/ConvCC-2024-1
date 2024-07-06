#include "data/symbol_table.h"

void SymbolTable::add_instance(std::string token, unsigned int line) {
    if (token_map.find(token) != token_map.end()) // tem o token
        token_map[token].push_back(line); // coloca a posição na tabela
    else
        token_map[token] = {line};
}

std::list<unsigned int> SymbolTable::get_instances(std::string token) { return token_map[token]; }