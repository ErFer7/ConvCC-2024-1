#pragma once

#include <string>

class Node {
    bool terminal;
    int type;  // may refer to enum Terminal or enum NonTerminal
    Node **children;
    std::string data;

    Node();
    void add_child(Node child);
    void add_child(int child);
};
