from __future__ import annotations

from enum import IntEnum
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, model_validator, constr, conset


Num = TypeVar("Num", int, float, str)


class VariableConstraintEnum(IntEnum):
    range = 1
    list = 2


class VariableRangeEnum(IntEnum):
    continuous = 1
    discrete = 2


class VariableRange(BaseModel):
    min: float | None = None
    max: float | None = None

    @model_validator(mode="after")
    def validate_range(self) -> VariableRange:
        if ((self.min is not None) ^ (self.max is not None)) or (
            self.min is not None and self.max is not None and self.min <= self.max
        ):
            return self
        raise ValueError("Invalid range!")


class ContinuousRange(VariableRange):
    pass


class DiscreteRange(VariableRange):
    min: int | None = None
    max: int | None = None


class VariableRangeConstraint(BaseModel):
    type: VariableRangeEnum
    range: ContinuousRange | DiscreteRange


class VariableListConstraint(BaseModel):
    items: conset(Num, min_length=1) | None


class Variable(BaseModel):
    name: constr(max_length=16)
    description: str | None = ""
    default: Any | None = ""
    constraint_type: VariableConstraintEnum | None = None
    constraint: VariableRangeConstraint | VariableListConstraint | None = None

    @model_validator(mode="after")
    def validate_constraint(self) -> Variable:
        if (
            (self.constraint_type is None and self.constraint is None)
            or (
                self.constraint_type == VariableConstraintEnum.range
                and type(self.constraint) == VariableRangeConstraint
            )
            or (
                self.constraint_type == VariableConstraintEnum.list
                and type(self.constraint) == VariableListConstraint
            )
        ):
            return self
        raise ValueError("Invalid constraint")


class VariableInDB(Variable):
    id: int
    formula_id: int


class OperatorEnum(IntEnum):
    plus = 1
    minus = 2
    multiply = 3
    divide = 4
    open_parentheses = 5
    close_parentheses = 6


class Operator(BaseModel):
    type: OperatorEnum
    name: str | None = None


class FormulaBase(BaseModel):
    name: constr(max_length=32)
    variables: list[Variable]


Token = TypeVar("Token", str, Operator)


class Formula(FormulaBase):
    tokens: list[Token]

    @model_validator(mode="after")
    def validate(self) -> Formula:
        variable_names = set()
        for variable in self.variables:
            if variable.name not in variable_names:
                variable_names.add(variable.name)
                continue
            raise ValueError("variable names must be unique!")
        for token in self.tokens:
            if type(token) is str and token not in variable_names:
                raise ValueError("Unknown variable")

        return self


class FormulaInDB(FormulaBase):
    id: int
    tree: list[Token]

    model_config = ConfigDict(from_attributes=True)


class VariableValue(BaseModel):
    name: constr(max_length=16)
    value: Num


class FormulaRun(BaseModel):
    formula_id: int
    variables: list[VariableValue]
