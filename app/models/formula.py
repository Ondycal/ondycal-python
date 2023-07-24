from enum import IntEnum
from typing import Any, List, Optional, Type, TypeVar, Union
from numbers import Number

from pydantic import BaseModel, ConfigDict, field_validator, root_validator


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

    @root_validator(skip_on_failure=True)
    def validate_range(cls, range):
        if ((range["min"] is not None) ^ (range["max"] is not None)) or (
            range["min"] is not None
            and range["max"] is not None
            and range["min"] <= range["max"]
        ):
            return range
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

    @root_validator(skip_on_failure=True)
    def validate_constraint(cls, variable):
        if (
            (variable["constraint_type"] is None and variable["constraint"] is None)
            or (
                variable["constraint_type"] == VariableConstraintEnum.range
                and type(variable["constraint"]) == VariableRangeConstraint
            )
            or (
                variable["constraint_type"] == VariableConstraintEnum.list
                and type(variable["constraint"]) == VariableListConstraint
            )
        ):
            return variable
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

    @root_validator(skip_on_failure=True)
    def validate_tokens(cls, formula):
        variable_names = set(variable.name for variable in formula["variables"])
        for token in formula["tokens"]:
            if type(token) is str and token not in variable_names:
                raise ValueError("Unknown variable")

        return formula
