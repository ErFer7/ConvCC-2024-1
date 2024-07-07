"""
Analisador Semântica
"""

from data.token import Token
from data.symbol_table import SymbolTable
from data.grammar import NonTerminalType as N, Terminal as T
from data.semantic_actions import *


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
