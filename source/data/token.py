"""
Definição de tokens.
"""

from data.grammar import Terminal


class Token:
    """
    Token.
    """

    type_: Terminal
    position: tuple[int, int]
    value: str

    def __init__(self, type_: Terminal, line: int, column: int, value: str = '') -> None:
        self.type_ = type_
        self.position = (line, column)
        self.value = value

    def __repr__(self) -> str:
        return f'<{self.type_.value}, {self.position}, {self.value}>'
