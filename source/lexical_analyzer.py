"""
Analisador léxico.
"""

from enum import Enum

from data.token import Token
from data.grammar import Terminal, STRING_TO_TERMINAL, ONE_CHAR_DEFINITIVE_TERMINALS
from symbol_table import SymbolTable

from return_status import LexicalReturnStatus

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

class LexicalAnalyzer:
    """
    Analisador léxico.
    """

    @staticmethod
    def analyze(source: str) -> tuple[LexicalReturnStatus, tuple[int,int], list[Token], SymbolTable]:
        """
        Analisa o código fonte e retorna a lista de tokens.
        """

        source += ' '
        symbol_table = SymbolTable()
        token_list: list[Token] = []
        state = LexicalAnalyzerStates.WHITE_SPACE
        current_line = 1
        current_column = 1
        token_column = 1
        index = 0
        current_token = ''

        while index < len(source):
            next_ = source[index]

            match (state):
                case LexicalAnalyzerStates.WHITE_SPACE:
                    if next_ in ' \n':
                        if next_ == '\n':
                            current_line += 1
                            current_column = 0

                        index += 1
                        current_column += 1
                    else:
                        state = LexicalAnalyzerStates.READ_SIMPLE
                case LexicalAnalyzerStates.READ_SIMPLE:
                    token_column = current_column

                    if next_.isalpha() or next_ == '_':
                        state = LexicalAnalyzerStates.MAYBE_IDENT
                        current_token += next_
                    elif next_.isdigit():
                        state = LexicalAnalyzerStates.NUMERAL
                        current_token += next_
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
                        # TODO: Otimizar isso aqui, daria pra só comparar pra ver se o next é um dos ONE_CHAR_DEFINITIVE_TERMINALS
                        if next_ in STRING_TO_TERMINAL and STRING_TO_TERMINAL[next_] in ONE_CHAR_DEFINITIVE_TERMINALS:
                            state = LexicalAnalyzerStates.WHITE_SPACE
                            token_list.append(Token(STRING_TO_TERMINAL[next_], current_line, token_column))
                        else:
                            return LexicalReturnStatus.INVALID_CHAR, (current_line,current_column), token_list, symbol_table

                    index += 1
                    current_column += 1
                case LexicalAnalyzerStates.MAYBE_IDENT:
                    if next_.isalnum() or next_ == '_':
                        current_token += next_
                        index += 1
                        current_column += 1
                    else:
                        state = LexicalAnalyzerStates.WHITE_SPACE

                        if current_token in STRING_TO_TERMINAL:
                            token_list.append(Token(STRING_TO_TERMINAL[current_token], current_line, token_column))
                        else:
                            token_list.append(Token(Terminal.IDENT, current_line, token_column, current_token))
                            symbol_table.add_symbol_instance(current_token, current_line, token_column)
                        current_token = ''
                case LexicalAnalyzerStates.NUMERAL:
                    if next_.isdigit():
                        current_token += next_
                        index += 1
                        current_column += 1
                    elif next_ == '.':
                        state = LexicalAnalyzerStates.FLOAT_FRACTIONAL
                        current_token += next_
                        index += 1
                        current_column += 1
                    elif next_.isalpha() or next_ == '_':
                        return LexicalReturnStatus.INVALID_NUMBER_FORMAT, (current_line,current_column), token_list, symbol_table
                    else:
                        state = LexicalAnalyzerStates.WHITE_SPACE
                        token_list.append(Token(Terminal.INT_CONST, current_line, token_column, current_token))
                        current_token = ''
                case LexicalAnalyzerStates.FLOAT_FRACTIONAL:
                    if next_.isdigit():
                        current_token += next_
                        index += 1
                        current_column += 1
                    elif next_.isalpha() or next_ == '_':
                        return LexicalReturnStatus.INVALID_NUMBER_FORMAT, (current_line,current_column), token_list, symbol_table
                    else:
                        state = LexicalAnalyzerStates.WHITE_SPACE
                        token_list.append(Token(Terminal.FLOAT_CONST, current_line, token_column, current_token))
                        current_token = ''
                case LexicalAnalyzerStates.STRING_LITERAL:
                    if next_ == '"':
                        state = LexicalAnalyzerStates.WHITE_SPACE
                        token_list.append(Token(Terminal.STRING_CONST, current_line, token_column, current_token))
                        current_token = ''
                    elif next_ == '\n':
                        return LexicalReturnStatus.UNCLOSED_STRING, (current_line,current_column), token_list, symbol_table
                    else:
                        current_token += next_

                    index += 1
                    current_column += 1
                case LexicalAnalyzerStates.ASSIGN_OR_EQUAL:
                    state = LexicalAnalyzerStates.WHITE_SPACE
                    if next_ == '=':
                        token_list.append(Token(Terminal.EQUAL, current_line, token_column))
                        index += 1
                        current_column += 1
                    else:
                        token_list.append(Token(Terminal.ASSIGNMENT, current_line, token_column))
                    current_token = ''
                case LexicalAnalyzerStates.GREATER_OR_GE:
                    state = LexicalAnalyzerStates.WHITE_SPACE
                    if next_ == '=':
                        token_list.append(Token(Terminal.GREATER_EQUAL, current_line, token_column))
                        index += 1
                        current_column += 1
                    else:
                        token_list.append(Token(Terminal.GREATER_THAN, current_line, token_column))
                    current_token = ''
                case LexicalAnalyzerStates.LESS_OR_LE:
                    state = LexicalAnalyzerStates.WHITE_SPACE
                    if next_ == '=':
                        token_list.append(Token(Terminal.LESS_EQUAL, current_line, token_column))
                        index += 1
                        current_column += 1
                    else:
                        token_list.append(Token(Terminal.LESS_THAN, current_line, token_column))
                    current_token = ''
                case LexicalAnalyzerStates.DIFFERENT:
                    state = LexicalAnalyzerStates.WHITE_SPACE
                    if next_ == '=':
                        token_list.append(Token(Terminal.NOT_EQUAL, current_line, token_column))
                        index += 1
                        current_column += 1
                    else:
                        return LexicalReturnStatus.INVALID_CHAR, (current_line,current_column), token_list, symbol_table
                    current_token = ''
                case _:
                    print('\n\nWhat\n\n')

        return LexicalReturnStatus.OK, (0,0), token_list, symbol_table
