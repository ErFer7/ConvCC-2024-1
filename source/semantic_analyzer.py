"""

"""

from data.token import Token
from data.symbol_table import SymbolTable
from data.grammar import NonTerminalType
from enum import Enum


class SemanticAction:
    """
    Ação semântica.
    """

    def __init__(self) -> None:
        pass

    def execute(self, token: Token, symbol_table: SymbolTable) -> None:
        """
        Executa a ação semântica.
        """
        pass


class SemanticReturnStatus(Enum):  # TODO: change error messages
    """
    Status de retorno do analisador semântico.
    """

    OK = 0
    ENTRY_DOES_NOT_EXIST = 1
    UNMATCHED_TERMINALS = 2
    STACK_NOT_EMPTY = 3


class SemanticAnalyzer:
    """
    Analisador semântico.
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

        pass
