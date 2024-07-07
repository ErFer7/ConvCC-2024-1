"""
Processador de SDT.
"""

from data.token import Token
from data.symbol_table import SymbolTable
from data.grammar import NonTerminalType
from syntax_analyzer import SyntaxAnalyzer, SyntaxReturnStatus
from semantic_analyzer import SemanticAction


class SDTProcessor:
    """
    Processador de SDT.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def process(tokens: list[Token], symbol_table: SymbolTable) -> tuple[SyntaxReturnStatus, Token]:
        """
        Processa a lista de tokens.
        """

        stack = []
        current_stack_element = NonTerminalType.PROGRAM  # Inicializa a stack com o símbolo inicial da gramática
        current_token_index = 0
        current_token = tokens[current_token_index]

        while True:
            if isinstance(current_stack_element, SemanticAction):
                current_stack_element.execute(tokens[current_token_index], symbol_table)  # TODO: change parameters after
            else:
                status, token_index_increment = SyntaxAnalyzer.analyze(
                    tokens[current_token_index],
                    symbol_table,
                    stack,
                    current_token_index,
                    current_stack_element
                )

                current_token_index += token_index_increment

                if status != SyntaxReturnStatus.OK:  # if not ok, return
                    return status, current_token

            if current_token_index == len(tokens):
                if len(stack) == 0:
                    return SyntaxReturnStatus.OK, current_token

                while stack:
                    status, token_index_increment = SyntaxAnalyzer.analyze(
                        '',
                        symbol_table,
                        stack,
                        current_token_index,
                        current_stack_element
                    )

                    current_token_index += token_index_increment

                    if status != SyntaxReturnStatus.OK:
                        return SyntaxReturnStatus.STACK_NOT_EMPTY, current_token

                return SyntaxReturnStatus.OK, current_token

            if len(stack) == 0:
                return SyntaxReturnStatus.ENTRY_NOT_CONSUMED, current_token

            current_token = tokens[current_token_index]
            current_stack_element = stack.pop()
