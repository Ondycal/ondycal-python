from enum import IntEnum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, field_validator, root_validator


class VariableConstraintEnum(IntEnum):
    range = 1
    list = 2


class VariableRangeEnum(IntEnum):
    continuous = 1
    discrete = 2


class ContinuousRange(BaseModel):
    min: Any
    max: Any


class DiscreteRange(ContinuousRange):
    type: Any


class VariableRangeConstraint(BaseModel):
    type: VariableRangeEnum
    range: Union[ContinuousRange, DiscreteRange]


class VariableListConstraint(BaseModel):
    items: List[Any]


class Variable(BaseModel):
    name: str
    description: Optional[str] = None
    default: Optional[Any] = None
    constraint_type: Optional[VariableConstraintEnum] = None
    constraint: Optional[
        Union[VariableRangeConstraint, VariableListConstraint]
    ] = None


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

    @field_validator('variables')
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
        variable_names = set(variable.name for variable in formula['variables'])
        for token in formula["tokens"]:
            if type(token) is str and token not in variable_names:
                raise ValueError("Unknown variable")

        return formula
