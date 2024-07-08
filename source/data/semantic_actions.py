from data.token import Token
from data.grammar import Terminal as T, NonTerminalType as N
import copy


class ArithmeticNode:
    _left: "ArithmeticNode"
    _right: "ArithmeticNode"

    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"{self.value}" + self.left + self.right


class ArithmeticTree:
    def __init__(self, root) -> None:
        self.root = root


class DerivationNode:
    symbol: N | Token | T
    children: list["DerivationNode"]
    no: ArithmeticNode
    parcial: ArithmeticNode
    type: T

    def __init__(self, symbol, parent=None) -> None:
        self.symbol = symbol
        self.parent = parent
        self.children = []
        self.no = None
        self.parcial = None
        self.visit_count = 0

    def add_children(self, node):
        self.children.append(node)

    def get_next(self):
        if not self.children and not self.parent:
            return self

        self.visit_count += 1
        if self.visit_count < len(self.children):
            return self.children[self.visit_count - 1]
        if self.parent:
            return self.parent
        return self


class DerivationTree:
    root: DerivationNode
    most_recent_node: DerivationNode

    def __init__(self, root) -> None:
        self.root = copy.copy(root)
        self.most_recent_node = self.root

    def create_nodes(self, parent, children_values):
        for value in children_values:
            if isinstance(value, T) or isinstance(value, N):
                new_node = DerivationNode(value, parent)
                parent.add_children(copy.copy(new_node))

    # def get_next_node(self):
    #     parent = self.most_recent_node.parent()
    #     list_of_children = parent.children
    #     curr_id = list_of_children.index(self.most_recent_node)
    #     if curr_id + 1 < len(parent.children):
    #         return list_of_children[curr_id + 1]

    def get_parent(self, node: DerivationNode):
        if node.parent:
            return node.parent
        return node


class SemanticAction:
    """
    Ação semântica.
    """

    def __init__(self, function) -> None:
        self.function = function

    def execute(self, node: DerivationNode) -> None:
        """
        Executa a ação semântica.
        """
        self.function(node)

    @staticmethod
    def get_arithmetic_value(token: Token):
        assert isinstance(token, Token)  # only debugging
        if token.value == "":
            return token.type_.value
        else:
            return token.value


def rule_right_synth(node: DerivationNode):
    node.no = node.children[-1].no


def rule_left_to_right(node: DerivationNode):
    node.children[1].parcial = node.children[0].no


def rule_left_synth(node: DerivationNode):
    node.no = node.children[0].no


def rule_parcial_inherit(node: DerivationNode):
    node.children[1].parcial = node.parcial


def rule_end_derivation(node: DerivationNode):
    node.no = node.parcial


def rule_create_empty(node: DerivationNode):
    token = node.symbol
    value = SemanticAction.get_arithmetic_value(token)
    new_arithmetic_node = ArithmeticNode(value, None, None)
    node.no = copy.deepcopy(new_arithmetic_node)


def rule7(node: DerivationNode):
    value = SemanticAction.get_arithmetic_value(node.children[0].symbol)
    left = node.parcial
    right = node.children[2].no
    new_arithmetic_node = ArithmeticNode(value, left, right)
    node.no = copy.deepcopy(new_arithmetic_node)


def rule8(node: DerivationNode):
    node.children[2] = node.children[1]


def rule9(node: DerivationNode):
    value = SemanticAction.get_arithmetic_value(node.children[0].symbol)
    left = node.children[1].parcial
    new_arithmetic_node = ArithmeticNode(value, left, None)
    node.children[1].no = copy.deepcopy(new_arithmetic_node)


def rule10(node: DerivationNode):
    value = SemanticAction.get_arithmetic_value(node.children[0].symbol)
    new_arithmetic_node = ArithmeticNode(value, None, None)
    node.parcial = copy.deepcopy(new_arithmetic_node)


def rule11(node: DerivationNode):
    node.parcial = node.children[0].no


def rule12(node: DerivationNode):
    node.no = node.children[1].no


def rule13(node: DerivationNode):  # para tratar LVALUE, a princípio
    value = SemanticAction.get_arithmetic_value(node.children[0].symbol)
    new_arithmetic_node = ArithmeticNode(value, None, None)
    node.no = copy.deepcopy(new_arithmetic_node)


# e os arrays????


# Semantic Actions declaration
action1 = SemanticAction(rule_right_synth)
action2 = SemanticAction(rule_left_to_right)
action3 = SemanticAction(rule_left_synth)
action4 = SemanticAction(rule_parcial_inherit)
action5 = SemanticAction(rule_end_derivation)
action6 = SemanticAction(rule_create_empty)
action7 = SemanticAction(rule7)
action8 = SemanticAction(rule8)
action9 = SemanticAction(rule9)
action10 = SemanticAction(rule10)
action11 = SemanticAction(rule11)
action12 = SemanticAction(rule12)
action13 = SemanticAction(rule13)


semantic_actions_dict = {
    1: action1,
    2: action2,
    3: action3,
    4: action4,
    5: action5,
    6: action6,
    7: action7,
    8: action8,
    9: action9,
    10: action10,
    11: action11,
    12: action12,
    13: action13,
}
