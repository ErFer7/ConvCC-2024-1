"""
Definição de tokens.
"""

from data.grammar import Terminal


class Token():
    """
    Token.
    """

    type_: Terminal
    line: int
    column: int
    value: str

    def __init__(self, type_: Terminal, line: int, column: int, value: str = '') -> None:
        self.type_ = type_
        self.line = line
        self.column = column
        self.value = value
