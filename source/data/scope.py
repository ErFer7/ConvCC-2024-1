"""
Escopo.
"""


class Scope:
    """
    Escopo.
    """

    id_: tuple[int]
    _next: int

    def __init__(self, id_: tuple[int] = (0,), next_: int = 0) -> None:
        self._id_ = id_
        self._next = next_

    def get_sub_scope(self) -> "Scope":
        """
        Retorna um subescopo.
        """

        return Scope(self.id_ + (self._next,), self._next + 1)

    def is_in_scope(self, scope: "Scope") -> bool:
        """
        Verifica se o escopo de um símbolo é um subescopo válido.
        """

        valid = True

        for i, id_level in enumerate(self.id_):
            if i < len(scope.id_):
                if id_level != scope.id_[i]:
                    valid = False
                    break
            else:
                valid = False
                break

        return valid
