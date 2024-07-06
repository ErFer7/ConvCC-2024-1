"""
Tabela de símbolos.
"""


class SymbolTable():
    """
    Tabela de símbolos.
    """

    _table: dict[str, int, int, str]  # name, line, column, value TODO: type, scope

    def __init__(self) -> None:
        self._table = {}
