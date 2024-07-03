#pragma once

#include <string>
#include <unordered_map>

#include "enums/return_codes.h"
#include "data/symbol_table.h"
#include "data/token_list.h"

enum TokenParserStates {
    WHITE_SPACE,       // You have been living here for as long as you can remember
    READ_SIMPLE,       // catches 1-char tokens, sends to other states
    MAYBE_IDENT,       // reads a word, then checks if it's a keyword
    NUMERAL,           // starts in a digit, may be int or float
    FLOAT_FRACTIONAL,  // fractional portion of float
    STRING_LITERAL,    // looks for string termination
    ASSIGN_OR_EQUAL,   // may find = or ==
    GREATER_OR_GE,     // may find > or >=
    LESS_OR_LE,        // may find < or <=
    DIFFERENT          // must find = after !
};

class LexicalAnalyzer {
   public:
    static LexicalReturnCode analyze(std::string source, TokenList &token_list, SymbolTable &symbol_table);

   private:
    static Terminal check_identifier(unsigned int line, std::string ident, SymbolTable &symbol_table);

   private:
    static const std::unordered_map<std::string, Terminal> _TOKEN_STRINGS;
};
