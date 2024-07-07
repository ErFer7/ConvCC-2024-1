"""

"""

from data.token import Token
from data.symbol_table import SymbolTable
from data.grammar import NonTerminalType as N, Terminal as T
from enum import Enum


class DerivationNode:
    _symbol: N | T
    _children: list['DerivationNode']
    

    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []
        self.no = None
        self.parcial= None

    def symbol(self):
        return self.symbol
    def children(self):
        return self.children
    def add_children(self,node):
        self.children.append(node)

class ArithmeticNode:
    _left: 'ArithmeticNode'
    _right: 'ArithmeticNode'
    
    def __init__(self, value, left = None, right = None) -> None:
        self.value = value
        self.left = left
        self.right = right

class ArithmeticTree:
    def __init__(self, root) -> None:
        self.root = root

class SemanticAction:
    """
    Ação semântica.
    """

    def __init__(self) -> None:
        pass

    def execute(self, node: DerivationNode) -> None:
        """
        Executa a ação semântica.
        """
        pass


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
