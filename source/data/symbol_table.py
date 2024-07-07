"""
Tabela de símbolos.
"""


class Symbol():
    """
    Símbolo.
    """

    _name: str
    _occurrences: list[tuple[int, int]]
    # TODO: Fix this
    _value: None
    _type: None
    _scope: None

    def __init__(self, name: str, first_occurrence: tuple[int, int]) -> None:
        self._name = name
        self._occurrences = [first_occurrence]

    def __repr__(self) -> str:
        return f'<{self._name}, {self._occurrences}>'

    def add_occurrence(self, occurrence: tuple[int, int]) -> None:
        """
        Adiciona uma ocorrência.
        """

        self._occurrences.append(occurrence)


class SymbolTable():
    """
    Tabela de símbolos.
    """

    _table: dict[str, Symbol]

    def __init__(self) -> None:
        self._table = {}

    def add_symbol_instance(self, name: str, line: int, column: int) -> None:
        """
        Adiciona um símbolo à tabela.
        """

        if name not in self._table:
            self._table[name] = Symbol(name, (line, column))
        else:
            self._table[name].add_occurrence((line, column))
