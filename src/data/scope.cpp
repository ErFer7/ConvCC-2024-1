#include "data/scope.h"

Scope::Scope(std::shared_ptr<Scope> parent, bool is_loop, unsigned int start_line, unsigned int start_column) {
    this->parent = parent;
    this->is_loop = is_loop;
    this->start_line = start_line;
    this->start_column = start_column;
}
