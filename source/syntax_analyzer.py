from typing import Any

from data.token import Token
from data.symbol_table import SymbolTable
from data.grammar import NonTerminalType, Terminal
from data.derivation_tables import DerivationTable, ProductionList
from return_status import SyntaxReturnStatus
from data.semantic_actions import SemanticAction


class SyntaxAnalyzer:
    """
    Analisador sintático.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def analyze(
        current_token: Token | str,
        symbol_table: SymbolTable,
        stack: list,
        current_token_index: int,
        current_stack_element: str | Terminal | NonTerminalType | SemanticAction | Any,
    ) -> tuple[SyntaxReturnStatus, int]:
        """
        Analisa a lista de tokens.
        """

        if current_token == "":
            # verificar se o fundo de pilha está na tabela
            if "" in DerivationTable[current_stack_element]:
                production_rules = ProductionList[
                    DerivationTable[current_stack_element][""]
                ].tail
                # se existe, adicionar as regras de produção na pilha
                stack.extend(production_rules[::-1])
                return SyntaxReturnStatus.OK, 0
            # se não existe a entrada na tabela de símbolos, retornar erro
            return SyntaxReturnStatus.ENTRY_DOES_NOT_EXIST, 0
        if isinstance(current_stack_element, Terminal):
            if current_token.type_ == current_stack_element:  # type: ignore
                return SyntaxReturnStatus.OK, 1
            return SyntaxReturnStatus.UNMATCHED_TERMINALS, 1
        if isinstance(current_stack_element, NonTerminalType):
            # verificar se a entrada existe na tabela de símbolos
            if current_token.type_ in DerivationTable[current_stack_element]:  # type: ignore
                production_rules = ProductionList[
                    DerivationTable[current_stack_element][current_token.type_]  # type: ignore
                ].tail
                # se existe, adicionar as regras de produção na pilha
                stack.extend(production_rules[::-1])
                return SyntaxReturnStatus.OK, 0
            # se não existe a entrada na tabela de símbolos, retornar erro
            return SyntaxReturnStatus.ENTRY_DOES_NOT_EXIST, 0
        return SyntaxReturnStatus.OK, 0
