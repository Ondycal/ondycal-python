from enum import IntEnum
from typing import Any, List, Optional, Type, TypeVar, Union
from numbers import Number

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


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
    name: str
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


class Operator(BaseModel):
    type: OperatorEnum
    name: Optional[str] = None


class Formula(BaseModel):
    name: str
    variables: List[Variable]
    tokens: List[Union[str, Operator]]

    @field_validator("variables")
    def unique_name_variables(cls, variables):
        unique_vars = set()
        for variable in variables:
            if variable.name not in unique_vars:
                unique_vars.add(variable.name)
                continue
            raise ValueError("variable names must be unique!")

        return variables

    @model_validator(mode="after")
    def validate_tokens(self) -> "Formula":
        variable_names = set(variable.name for variable in self.variables)
        for token in self.tokens:
            if type(token) is str and token not in variable_names:
                raise ValueError("Unknown variable")

        return self
