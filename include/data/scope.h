#pragma once

#include <list>
#include <memory>

class Scope {
   public:
    Scope(std::shared_ptr<Scope> parent, bool is_loop, unsigned int start_line, unsigned int start_column);

    void add_child(std::unique_ptr<Scope> child);
    std::shared_ptr<Scope> get_parent();

   private:
    std::shared_ptr<Scope> parent;
    std::list<std::unique_ptr<Scope>> children;
    bool is_loop;
    unsigned int start_line;
    unsigned int start_column;
};
