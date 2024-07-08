"""
Tabela de símbolos.
"""

from data.scope import Scope
from data.grammar import Terminal
from return_status import SemanticReturnStatus


class Symbol:
    """
    Símbolo.
    """

    _name: str
    position: tuple[int, int]
    scope: Scope | None
    type_: Terminal | None
    value: int | float | str | None
    _is_declaration: bool

    def __init__(self, name: str, occurrence: tuple[int, int]) -> None:
        self._name = name
        self.position = occurrence
        self.scope = None
        self.type_ = None
        self.value = None
        self._is_declaration = False

    def __repr__(self) -> str:
        return f"<{self._name}, {self.position}>"

    @property
    def is_declaration(self) -> bool:
        """
        Retorna se é uma declaração.
        """

        return self._is_declaration

    def set_as_declaration(self) -> None:
        """
        Define que o símbolo é uma declaração.
        """

        self._is_declaration = True


class SymbolTable:
    """
    Tabela de símbolos.
    """

    _table: dict[str, list[Symbol]]

    def __init__(self) -> None:
        self._table = {}

    def __repr__(self) -> str:
        return f"{self._table}"

    def add_symbol_instance(self, name: str, line: int, column: int) -> None:
        """
        Adiciona um símbolo à tabela.
        """

        if name not in self._table:
            self._table[name] = [Symbol(name, (line, column))]
        else:
            self._table[name].append(Symbol(name, (line, column)))

    def set_symbol_scope(self, name: str, line: int, column: int, scope: Scope) -> None:
        """
        Define o escopo de um símbolo.
        """

        for symbol in self._table[name]:
            if symbol.position == (line, column):
                symbol.scope = scope

    def set_symbol_type(
        self, name: str, line: int, column: int, type_: Terminal
    ) -> None:
        """
        Define o tipo de um símbolo.
        """

        for symbol in self._table[name]:
            if symbol.position == (line, column):
                symbol.type_ = type_

    def set_symbol_value(
        self, name: str, line: int, column: int, value: int | float | str
    ) -> None:
        """
        Define o valor de um símbolo.
        """

        for symbol in self._table[name]:
            if symbol.position == (line, column):
                symbol.value = value

    def check_scope_validity(
        self, name: str, line: int, column: int
    ) -> SemanticReturnStatus:
        """
        Verifica se um símbolo está em um escopo válido.
        """

        symbol_instance = None

        for symbol in self._table[name]:
            if symbol.position == (line, column):
                symbol_instance = symbol

        symbol_declarations = []

        for symbol in self._table[name]:
            if symbol.is_declaration:
                symbol_declarations.append(symbol)

        # Se o símbolo é uma declaração, verifica se algum outro
        # símbolo com o mesmo nome já foi declarado no mesmo escopo ou num escopo superior
        if symbol_instance.is_declaration:
            for declaration in symbol_declarations:
                if declaration.position != symbol_instance.position:
                    if declaration.scope.is_in_scope(symbol_instance.scope):
                        return SemanticReturnStatus.DOUBLE_DECLARATION
            return SemanticReturnStatus.OK

        # Se o símbolo é apenas usado, verifica se há uma declaração no mesmo
        # escopo ou num escopo superior
        for declaration in symbol_declarations:
            if declaration.scope.is_in_scope(symbol_instance.scope):
                return SemanticReturnStatus.OK

        return SemanticReturnStatus.UNDECLARED_SYMBOL
