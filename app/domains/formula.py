from enum import IntEnum
from typing import Any, List, Optional, Type, TypeVar, Union
from numbers import Number

from pydantic import BaseModel, ConfigDict, model_validator, constr


Num = TypeVar("Num", bound=Number)


class ArbitraryTypeModel(BaseModel):
    # TODO: improve code after pydantic update
    model_config = ConfigDict(arbitrary_types_allowed=True)


class VariableConstraintEnum(IntEnum):
    range = 1
    list = 2


class VariableRangeEnum(IntEnum):
    continuous = 1
    discrete = 2


class ContinuousRange(ArbitraryTypeModel):
    min: Optional[Num] = None
    max: Optional[Num] = None

    @model_validator(mode="after")
    def validate_range(self) -> "ContinuousRange":
        if ((self.min is not None) ^ (self.max is not None)) or (
            self.min is not None and self.max is not None and self.min <= self.max
        ):
            return self
        raise ValueError("Invalid range!")


class DiscreteRange(ContinuousRange):
    type: Type[Num]


class VariableRangeConstraint(BaseModel):
    type: VariableRangeEnum
    range: Union[ContinuousRange, DiscreteRange]


class VariableListConstraint(ArbitraryTypeModel):
    items: List[Union[Num, str]]


VariableConstraint = TypeVar(
    "VariableConstraint", VariableRangeConstraint, VariableListConstraint
)


class Variable(BaseModel):
    name: constr(max_length=16)
    description: Optional[str] = None
    default: Optional[Any] = None
    constraint_type: Optional[VariableConstraintEnum] = None
    constraint: Optional[VariableConstraint] = None

    @model_validator(mode="after")
    def validate_constraint(self) -> "Variable":
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


class OperatorEnum(IntEnum):
    plus = 1
    minus = 2
    multiply = 3
    divide = 4
    open_parentheses = 5
    close_parentheses = 6


class Operator(BaseModel):
    type: OperatorEnum
    name: Optional[str] = None


class Formula(BaseModel):
    name: constr(max_length=32)
    variables: List[Variable]
    tokens: List[Union[str, Operator]]

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate(self) -> "Formula":
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


class VariableValue(ArbitraryTypeModel):
    name: constr(max_length=16)
    value: Num


class FormulaRun(BaseModel):
    formula_id: int
    variables: List[VariableValue]
