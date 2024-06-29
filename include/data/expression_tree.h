#include <string>

#ifndef EXPRESSION_TREE_H
#define EXPRESSION_TREE_H

class Node {
    bool terminal;
    int type; // may refer to enum Terminal or enum NonTerminal
    Node **children;
    std::string data;

    Node();
    void add_child(Node child);
    void add_child(int child);
};

#endif