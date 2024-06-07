#include <list>
#include <string>
#ifndef TOKEN_LIST_H
#define TOKEN_LIST_H

struct Token {
    int type;
    std::string data;
};

class TokenList {
    public:
        void push_back(int type, std::string info = "");
        Token pop_front();
        bool empty();
    private:
        std::list<Token> internal_token_list;
};
#endif