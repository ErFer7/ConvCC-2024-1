#pragma once

#include <list>
#include <string>

#include "enums/grammar_symbols.h"

struct Token {
    Terminal type;
    unsigned int line;
    unsigned int column;
    std::string data;
};

class TokenList {
   public:
    void push_back(Terminal type, unsigned int line, unsigned int column, std::string data = "");
    Token pop_front();
    bool empty();

   private:
    std::list<Token> _internal_token_list;
};
