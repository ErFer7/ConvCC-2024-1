"""
Processador de SDT.
"""

from data.token import Token
from data.symbol_table import SymbolTable
from data.grammar import Terminal, NonTerminalType
from syntax_analyzer import SyntaxAnalyzer, SyntaxReturnStatus
from semantic_analyzer import SemanticAnalyzer, SemanticAction


class SDTProcessor:
    """
    Processador de SDT.
    """

    def __init__(self) -> None:
        pass

    def process(
        self, tokens: list[Token], symbol_table: SymbolTable
    ) -> SyntaxReturnStatus:
        """
        Processa a lista de tokens.
        """

        stack = []
        current_index_token = 0
        current_stack_element = (
            NonTerminalType.PROGRAM
        )  # Inicializa a stack com o símbolo inicial da gramática
        current_token = tokens[current_index_token]

        while True:
            if isinstance(current_stack_element, SemanticAction):
                current_stack_element.execute(
                    tokens[current_index_token], symbol_table
                )  # TODO: change parameters after
            else:
                status = SyntaxAnalyzer.analyze(
                    tokens[current_index_token],
                    symbol_table,
                    stack,
                    current_index_token,
                )
                if status != SyntaxReturnStatus.OK:  # if not ok, return
                    return status, current_token

            if current_index_token == len(tokens):
                if len(stack) == 0:
                    return SyntaxReturnStatus.OK, current_token
                else:
                    while stack:
                        status = SyntaxAnalyzer.analyze(
                        "",
                        symbol_table,
                        stack,
                        current_index_token,
                    )
                        if status != SyntaxReturnStatus.OK:
                            return SyntaxReturnStatus.STACK_NOT_EMPTY, current_token
                    return SyntaxReturnStatus.OK, current_token

            if len(stack) == 0:
                return SyntaxReturnStatus.ENTRY_NOT_CONSUMED, current_token

            current_token = tokens[current_index_token]
            current_stack_element = stack.pop(0)
