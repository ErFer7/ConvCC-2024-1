"""
Processador de SDT.
"""

from data.token import Token
from data.symbol_table import SymbolTable


class SDTProcessor():
    """
    Processador de SDT.
    """

    def __init__(self) -> None:
        pass

    def process(self, tokens: list[Token], symbol_table: SymbolTable) -> None:
        """
        Processa a lista de tokens.
        """

        stack = []

        for token in tokens:
            