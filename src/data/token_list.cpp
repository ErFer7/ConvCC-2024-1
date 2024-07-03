#include "data/token_list.h"

#include "enums/grammar_symbols.h"

void TokenList::push_back(Terminal type, std::string data) {
    struct Token token = {type, data};
    _internal_token_list.push_back(token);
};

Token TokenList::pop_front() {
    Token token = _internal_token_list.front();
    _internal_token_list.pop_front();
    return token;
};

bool TokenList::empty() { return _internal_token_list.empty(); };