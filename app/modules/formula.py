from utils.formula import create_expression_tree
from domains import FormulaModel


def formula_create(formula: FormulaModel):
    create_expression_tree(formula.tokens)
