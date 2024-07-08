"""
Status de retorno.
"""

from enum import Enum
from data.token import Token


class LexicalReturnStatus(Enum):
    """
    Status de retorno do analisador léxico.
    """

    OK = 0
    INVALID_CHAR = 1
    INVALID_NUMBER_FORMAT = 2
    UNCLOSED_STRING = 3


class SyntaxReturnStatus(Enum):
    """
    Status de retorno do analisador sintático.
    """

    OK = 0
    ENTRY_DOES_NOT_EXIST = 1
    UNMATCHED_TERMINALS = 2
    STACK_NOT_EMPTY = 3
    ENTRY_NOT_CONSUMED = 4


class SemanticReturnStatus(Enum):  # TODO: change error messages
    """
    Status de retorno do analisador semântico.
    """

    OK = 0
    UNDECLARED_SYMBOL = 1
    DOUBLE_DECLARATION = 2
    TYPE_MISMATCH = 3


class ReturnStatus:
    """
    Status de retorno.
    """

    _status: LexicalReturnStatus | SyntaxReturnStatus | SemanticReturnStatus
    _return_object: Token | None
    _position: tuple[int, int]  # Linha, coluna

    def __init__(
        self,
        status: LexicalReturnStatus | SyntaxReturnStatus | SemanticReturnStatus,
        return_object: Token | None,
        position: tuple[int, int] | None = None,
    ) -> None:
        self._status = status
        self._return_object = return_object

        if self._return_object is not None:
            self._position = return_object.position  # type: ignore
        elif position is not None:
            self._position = position

    def has_errors(self) -> bool:
        """
        Retorna se a compilação funcionou.
        """

        return self._status not in (
            LexicalReturnStatus.OK,
            SyntaxReturnStatus.OK,
            SemanticReturnStatus.OK,
        )

    def get_message(self) -> str:
        """
        Mensagem de retorno.
        """

        match self._status:
            case (
                LexicalReturnStatus.OK | SyntaxReturnStatus.OK | SemanticReturnStatus.OK
            ):
                return "The program compiled successfully"

            case LexicalReturnStatus.INVALID_CHAR:
                return (
                    f'Invalid character "{self._return_object}" in line {self._position[0]},'
                    f" column {self._position[1]}"
                )
            case LexicalReturnStatus.INVALID_NUMBER_FORMAT:
                return f"Invalid number format at line {self._position[0]}, column {self._position[1]}."
            case LexicalReturnStatus.UNCLOSED_STRING:
                return f"Unclosed string at the end of line {self._position[0]}."

            case SyntaxReturnStatus.ENTRY_DOES_NOT_EXIST:
                return f'Unable to parse entry at line {self._position[0]}, column {self._position[1]}. Found "{self._return_object.type_.value}"'
            case SyntaxReturnStatus.UNMATCHED_TERMINALS:
                return f"Unable to parse entry at line {self._position[0]}, column {self._position[1]}."
            case SyntaxReturnStatus.STACK_NOT_EMPTY:
                return f"Unable to parse entry at line {self._position[0]}, column {self._position[1]}."
            case SyntaxReturnStatus.ENTRY_NOT_CONSUMED:
                return (
                    "Finished parsing before end of file, cannot process "
                    f"past line {self._position[0]}, column {self._position[1]}"
                )

            # TODO: Adicionar todos os casos de erro
            case _:
                return ""
