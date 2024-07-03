#pragma once

#include <list>
#include <string>

#include "enums/grammar_symbols.h"

struct Token {
    Terminal type;
    std::string data;
};

class TokenList {
   public:
    void push_back(Terminal type, std::string data = "");
    Token pop_front();
    bool empty();

   private:
    std::list<Token> _internal_token_list;
};
