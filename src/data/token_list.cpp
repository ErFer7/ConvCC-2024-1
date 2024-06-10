#include "data/token_list.h"
#include "data/grammar_symbols.h"

void TokenList::push_back(Symbols type, std::string info) {
    struct Token token = {type,info};
    internal_token_list.push_back(token);
};

Token TokenList::pop_front() {
    Token token = internal_token_list.front(); 
    internal_token_list.pop_front();
    return token;
};

bool TokenList::empty() {
    return internal_token_list.empty();
};