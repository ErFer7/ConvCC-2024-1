from data.token import Token
from data.symbol_table import SymbolTable
from enum import Enum
from data.grammar import NonTerminalType, Terminal
from data.derivation_tables import DerivationTable, ProductionList


class SyntaxReturnStatus(Enum):
    """
    Status de retorno do analisador sintático.
    """

    OK = 0
    ENTRY_DOES_NOT_EXIST = 1
    UNMATCHED_TERMINALS = 2
    STACK_NOT_EMPTY = 3
    ENTRY_NOT_CONSUMED = 4


class SyntaxAnalyzer:
    """
    Analisador sintático.
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def analyze(
        current_token: Token,
        symbol_table: SymbolTable,
        stack: list,
        current_id_token: int,
    ) -> None:
        """
        Analisa a lista de tokens.
        """
        if current_token == "":
            # verificar se o fundo de pilha está na tabela
            if "" in DerivationTable[stack[0]]:
                production_rules = ProductionList[
                    DerivationTable[stack[0]][""]
                ].tail
                # se existe, adicionar as regras de produção na pilha
                stack = production_rules + stack
                return SyntaxReturnStatus.OK
            # se não existe a entrada na tabela de símbolos, retornar erro
            return SyntaxReturnStatus.ENTRY_DOES_NOT_EXIST
        if isinstance(stack[0], Terminal):
            if current_token.type_ == stack[0]:
                current_id_token += 1
                return SyntaxReturnStatus.OK
            return SyntaxReturnStatus.UNMATCHED_TERMINALS
        if isinstance(stack[0], NonTerminalType):
            # verificar se a entrada existe na tabela de símbolos
            if current_token.type_ in DerivationTable[stack[0]]:
                production_rules = ProductionList[
                    DerivationTable[stack[0]][current_token.type_]
                ].tail
                # se existe, adicionar as regras de produção na pilha
                stack = production_rules + stack
                return SyntaxReturnStatus.OK
            # se não existe a entrada na tabela de símbolos, retornar erro
            return SyntaxReturnStatus.ENTRY_DOES_NOT_EXIST
