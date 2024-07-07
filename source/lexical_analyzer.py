"""
Analisador léxico.
"""

from enum import Enum

from data.token import Token
from data.grammar import Terminal, STRING_TO_TERMINAL, ONE_CHAR_DEFINITIVE_TERMINALS
from data.symbol_table import SymbolTable


class LexicalAnalyzerStates(Enum):
    """
    Estados da análise.
    """

    WHITE_SPACE = 0       # You have been living here for as long as you can remember
    READ_SIMPLE = 1       # catches 1-char tokens, sends to other states
    MAYBE_IDENT = 2       # reads a word, then checks if it's a keyword
    NUMERAL = 3           # starts in a digit, may be int or float
    FLOAT_FRACTIONAL = 4  # fractional portion of float
    STRING_LITERAL = 5    # looks for string termination
    ASSIGN_OR_EQUAL = 6   # may find = or ==
    GREATER_OR_GE = 7     # may find > or >=
    LESS_OR_LE = 8        # may find < or <=
    DIFFERENT = 9         # must find = after !


class LexicalReturnStatus(Enum):
    """
    Status de retorno do analisador léxico.
    """

    OK = 0
    INVALID_CHAR = 1
    INVALID_NUMBER_FORMAT = 2
    UNCLOSED_STRING = 3


class LexicalAnalyzer:
    """
    Analisador léxico.
    """

    @staticmethod
    def analyze(source: str) -> tuple[LexicalReturnStatus, str, list[Token], SymbolTable]:
        """
        Analisa o código fonte e retorna a lista de tokens.
        """

        symbol_table = SymbolTable()
        token_list: list[Token] = []
        state = LexicalAnalyzerStates.WHITE_SPACE
        line = 1
        column = 1
        token_column = 1
        index = 0
        token = ''

        while index < len(source):
            next_ = source[index]

            match (state):
                case LexicalAnalyzerStates.WHITE_SPACE:
                    if next_ in ' \n':
                        if next_ == '\n':
                            line += 1
                            column = 0

                        index += 1
                        column += 1
                    else:
                        state = LexicalAnalyzerStates.READ_SIMPLE
                case LexicalAnalyzerStates.READ_SIMPLE:
                    token_column = column

                    if next_.isalpha() or next_ == '_':
                        state = LexicalAnalyzerStates.MAYBE_IDENT
                        token += next_
                    elif next_.isdigit():
                        state = LexicalAnalyzerStates.NUMERAL
                        token += next_
                    elif next_ == '"':
                        state = LexicalAnalyzerStates.STRING_LITERAL
                    elif next_ == '=':
                        state = LexicalAnalyzerStates.ASSIGN_OR_EQUAL
                    elif next_ == '>':
                        state = LexicalAnalyzerStates.GREATER_OR_GE
                    elif next_ == '<':
                        state = LexicalAnalyzerStates.LESS_OR_LE
                    elif next_ == '!':
                        state = LexicalAnalyzerStates.DIFFERENT
                    else:
                        if next_ in STRING_TO_TERMINAL and STRING_TO_TERMINAL[next_] in ONE_CHAR_DEFINITIVE_TERMINALS:
                            state = LexicalAnalyzerStates.WHITE_SPACE
                            token_list.append(Token(STRING_TO_TERMINAL[next_], line, token_column))
                        else:
                            return LexicalReturnStatus.INVALID_CHAR, next_, token_list, symbol_table

                    index += 1
                    column += 1
                case LexicalAnalyzerStates.MAYBE_IDENT:
                    if next_.isalnum() or next_ == '_':
                        token += next_
                        index += 1
                        column += 1
                    else:
                        state = LexicalAnalyzerStates.WHITE_SPACE

                        if token in STRING_TO_TERMINAL:
                            token_list.append(Token(STRING_TO_TERMINAL[token], line, token_column))
                        else:
                            token_list.append(Token(Terminal.IDENT, line, token_column, token))
                            symbol_table.add_symbol_instance(token, line, token_column)
                        token = ''
                case LexicalAnalyzerStates.NUMERAL:
                    if next_.isdigit():
                        token += next_
                        index += 1
                        column += 1
                    elif next_ == '.':
                        state = LexicalAnalyzerStates.FLOAT_FRACTIONAL
                        token += next_
                        index += 1
                        column += 1
                    elif next_.isalpha() or next_ == '_':
                        return LexicalReturnStatus.INVALID_NUMBER_FORMAT, next_, token_list, symbol_table
                    else:
                        state = LexicalAnalyzerStates.WHITE_SPACE
                        token_list.append(Token(Terminal.INT_CONST, line, token_column, token))
                        token = ''
                case LexicalAnalyzerStates.FLOAT_FRACTIONAL:
                    if next_.isdigit():
                        token += next_
                        index += 1
                        column += 1
                    elif next_.isalpha() or next_ == '_':
                        return LexicalReturnStatus.INVALID_NUMBER_FORMAT, next_, token_list, symbol_table
                    else:
                        state = LexicalAnalyzerStates.WHITE_SPACE
                        token_list.append(Token(Terminal.FLOAT_CONST, line, token_column, token))
                        token = ''
                case LexicalAnalyzerStates.STRING_LITERAL:
                    if next_ == '"':
                        state = LexicalAnalyzerStates.WHITE_SPACE
                        token_list.append(Token(Terminal.STRING_CONST, line, token_column, token))
                        token = ''
                    elif next_ == '\n':
                        return LexicalReturnStatus.UNCLOSED_STRING, next_, token_list, symbol_table
                    else:
                        token += next_

                    index += 1
                    column += 1
                case LexicalAnalyzerStates.ASSIGN_OR_EQUAL:
                    state = LexicalAnalyzerStates.WHITE_SPACE
                    if next_ == '=':
                        token_list.append(Token(Terminal.EQUAL, line, token_column))
                        index += 1
                        column += 1
                    else:
                        token_list.append(Token(Terminal.ASSIGNMENT, line, token_column))
                    token = ''
                case LexicalAnalyzerStates.GREATER_OR_GE:
                    state = LexicalAnalyzerStates.WHITE_SPACE
                    if next_ == '=':
                        token_list.append(Token(Terminal.GREATER_EQUAL, line, token_column))
                        index += 1
                        column += 1
                    else:
                        token_list.append(Token(Terminal.GREATER_THAN, line, token_column))
                    token = ''
                case LexicalAnalyzerStates.LESS_OR_LE:
                    state = LexicalAnalyzerStates.WHITE_SPACE
                    if next_ == '=':
                        token_list.append(Token(Terminal.LESS_EQUAL, line, token_column))
                        index += 1
                        column += 1
                    else:
                        token_list.append(Token(Terminal.LESS_THAN, line, token_column))
                    token = ''
                case LexicalAnalyzerStates.DIFFERENT:
                    state = LexicalAnalyzerStates.WHITE_SPACE
                    if next_ == '=':
                        token_list.append(Token(Terminal.NOT_EQUAL, line, token_column))
                        index += 1
                        column += 1
                    else:
                        return LexicalReturnStatus.INVALID_CHAR, next_, token_list, symbol_table
                    token = ''
                case _:
                    print('\n\nWhat\n\n')

        return LexicalReturnStatus.OK, '', token_list, symbol_table
