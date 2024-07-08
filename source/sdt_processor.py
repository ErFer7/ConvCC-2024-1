"""
Processador de SDT.
"""

from typing import Any

from data.token import Token
from symbol_table import SymbolTable

from data.grammar import NonTerminalType, Terminal
from data.derivation_tables import DerivationTable, ProductionList
from return_status import SyntaxReturnStatus
from data.semantic_actions import SemanticAction, DerivationTree, DerivationNode


class SDTProcessor:
    """
    Processador de SDT.
    """

    _derivation_tree: DerivationTree

    def __init__(self) -> None:
        self._derivation_tree = None

    def add_to_stack(
        self, stack: list, productions: list, curr_node: DerivationNode
    ) -> None:
        self._derivation_tree.create_nodes(curr_node, productions)
        stack.extend(productions[::-1])

    def init_derivation_tree(self, root_val) -> None:
        root = DerivationNode(root_val, None)
        self._derivation_tree = DerivationTree(root)

    def process(
        self, tokens: list[Token], symbol_table: SymbolTable
    ) -> tuple[SyntaxReturnStatus, Token]:
        """
        Processa a lista de tokens.
        """

        stack = []
        # Inicializa a stack com o símbolo inicial da gramática
        current_stack_element = NonTerminalType.PROGRAM

        current_token_index = 0
        current_token = tokens[current_token_index]

        self.init_derivation_tree(current_stack_element)
        current_derivation_node = self._derivation_tree.root

        while True:
            if isinstance(current_stack_element, SemanticAction):
                current_stack_element.execute(
                    current_derivation_node
                )  # TODO: change parameters after
            else:

                current_derivation_node = current_derivation_node.get_next()

                status, token_index_increment = self.process_token(
                    tokens[current_token_index],
                    symbol_table,
                    stack,
                    current_token_index,
                    current_stack_element,
                    current_derivation_node,
                )

                current_token_index += token_index_increment

                if status != SyntaxReturnStatus.OK:  # if not ok, return
                    return status, current_token

            if current_token_index == len(tokens):
                if len(stack) == 0:
                    return SyntaxReturnStatus.OK, current_token

                while stack:
                    current_stack_element = stack.pop()

                    status, token_index_increment = self.process_token(
                        "",
                        symbol_table,
                        stack,
                        current_token_index,
                        current_stack_element,
                        current_derivation_node,
                    )

                    current_token_index += token_index_increment

                    if status != SyntaxReturnStatus.OK:
                        return SyntaxReturnStatus.STACK_NOT_EMPTY, current_token

                return SyntaxReturnStatus.OK, current_token

            if len(stack) == 0:
                return SyntaxReturnStatus.ENTRY_NOT_CONSUMED, current_token

            current_token = tokens[current_token_index]
            current_stack_element = stack.pop()

            # new_node = DerivationNode(current_stack_element)
            # current_derivation_node.add_children(new_node)
            # current_derivation_node = new_node

    def process_token(
        self,
        current_token: Token | str,
        symbol_table: SymbolTable,
        stack: list,
        current_token_index: int,
        current_stack_element: str | Terminal | NonTerminalType | SemanticAction | Any,
        current_derivation_node: DerivationNode,
    ) -> tuple[SyntaxReturnStatus, int]:
        """
        Analisa a lista de tokens.
        """

        if current_token == "":
            # verificar se o fundo de pilha está na tabela
            if (
                not isinstance(current_stack_element, Terminal)
                and "" in DerivationTable[current_stack_element]
            ):
                production_rules = ProductionList[
                    DerivationTable[current_stack_element][""]
                ].tail

                # se existe, adicionar as regras de produção na pilha
                # stack.extend(production_rules[::-1])
                self.add_to_stack(stack, production_rules, current_derivation_node)
                current_derivation_node = self._derivation_tree.get_parent()
                return SyntaxReturnStatus.OK, 0
            # se não existe a entrada na tabela de símbolos, retornar erro
            return SyntaxReturnStatus.ENTRY_DOES_NOT_EXIST, 0
        if isinstance(current_stack_element, Terminal):
            if current_token.type_ == current_stack_element:  # type: ignore

                current_derivation_node.symbol = current_token  # change to token
                return SyntaxReturnStatus.OK, 1
            return SyntaxReturnStatus.UNMATCHED_TERMINALS, 1
        if isinstance(current_stack_element, NonTerminalType):
            # verificar se a entrada existe na tabela de símbolos
            if current_token.type_ in DerivationTable[current_stack_element]:  # type: ignore
                production_rules = ProductionList[
                    DerivationTable[current_stack_element][current_token.type_]  # type: ignore
                ].tail

                # se existe, adicionar as regras de produção na pilha
                # stack.extend(production_rules[::-1])
                self.add_to_stack(stack, production_rules, current_derivation_node)
                return SyntaxReturnStatus.OK, 0
            # se não existe a entrada na tabela de símbolos, retornar erro
            return SyntaxReturnStatus.ENTRY_DOES_NOT_EXIST, 0
        return SyntaxReturnStatus.OK, 0
