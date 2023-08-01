from __future__ import annotations

from typing import TypeVar

from app.domains.formula import Operator, OperatorEnum


class Node:
    def __init__(
        self, value: str | Operator = None, left: Node = None, right: Node = None
    ) -> None:
        self.value = value
        self.left = left
        self.right = right


EN = TypeVar("EN", str, Operator, Node)


def last_occurrence(tokens: list[EN], element: str | Operator) -> int:
    for i, token in reversed(list(enumerate(tokens))):
        if (
            type(element) is Operator and getattr(token, "type", None) is element.type
        ) or (type(element) is str and element == token):
            return i

    return -1


def create_variable_expression(tokens: list[EN]) -> Node:
    if len(tokens) != 1 or type(tokens[0]) is Operator:
        raise ValueError("Invalid formula")

    token = tokens[0]
    match type(token).__name__:
        case "Node":
            return token
        case "str":
            return Node(token)
        case _:
            raise ValueError("Invalid formula")


def create_multiply_expression_tree(tokens: list[EN]) -> Node:
    last_multiply_op_index: int = last_occurrence(
        tokens, Operator(type=OperatorEnum.multiply)
    )
    if last_multiply_op_index == -1:
        return create_variable_expression(tokens)
    if last_multiply_op_index in (0, len(tokens) - 1):
        raise ValueError("Invalid formula")

    node = Node(tokens[last_multiply_op_index])
    node.left = create_multiply_expression_tree(tokens[:last_multiply_op_index])
    node.right = create_variable_expression(tokens[last_multiply_op_index + 1 :])
    return node


# http://www.cs.ecu.edu/karl/5220/spr16/Notes/CFG/precedence.html
def create_expression_tree(tokens: list[EN]) -> Node:
    last_sum_op_index: int = last_occurrence(tokens, Operator(type=OperatorEnum.plus))
    if last_sum_op_index == -1:
        return create_multiply_expression_tree(tokens)
    if last_sum_op_index in (0, len(tokens) - 1):
        raise ValueError("Invalid formula")

    node = Node(tokens[last_sum_op_index])
    node.left = create_expression_tree(tokens[:last_sum_op_index])
    node.right = create_multiply_expression_tree(tokens[last_sum_op_index + 1 :])
    return node
