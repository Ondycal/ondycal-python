from __future__ import annotations

import datetime

from sqlalchemy import (
    BigInteger,
    Enum,
    ForeignKey,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base_class import Base
from app.domains import VariableConstraintEnum, VariableRangeEnum


class Formula(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now, nullable=False
    )
    updated: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now, nullable=False
    )
    tree: Mapped[dict] = mapped_column(JSON, nullable=False, default={})

    variables: Mapped[list[Variable]] = relationship(back_populates="formula_id")


class Variable(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    formula_id: Mapped[int] = mapped_column(ForeignKey("formula.id"), index=True)
    name: Mapped[str] = mapped_column(String(16), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    default: Mapped[str] = mapped_column(Text)
    constraint_type: Mapped[VariableConstraintEnum] = mapped_column(
        Enum(VariableConstraintEnum)
    )

    variable_constraint_range: Mapped[VariableRangeConstraint] = relationship(
        back_populates="range_constraint", uselist=False
    )
    variable_constraint_list: Mapped[VariableListConstraint] = relationship(
        back_populates="list_constraint", uselist=False
    )


class VariableRangeConstraint(Base):
    id: Mapped[int] = mapped_column(ForeignKey("variable.id"), primary_key=True)
    type: Mapped[VariableRangeEnum] = mapped_column(
        Enum(VariableRangeEnum), nullable=False
    )

    continuous_range: Mapped[VariableContinuousRangeConstraint] = relationship(
        back_populates="continuous_constraint",
        uselist=False,
    )
    discrete_range: Mapped[VariableDiscreteRangeConstraint] = relationship(
        back_populates="discrete_constraint",
        uselist=False,
    )


class VariableContinuousRangeConstraint(Base):
    id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variablerangeconstraint.id"), primary_key=True
    )
    min: Mapped[float | None] = mapped_column(nullable=True)
    max: Mapped[float | None] = mapped_column(nullable=True)


class VariableDiscreteRangeConstraint(Base):
    id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("variablerangeconstraint.id"), primary_key=True
    )
    min: Mapped[int | None] = mapped_column(nullable=True)
    max: Mapped[int | None] = mapped_column(nullable=True)


class VariableListConstraint(Base):
    id: Mapped[int] = mapped_column(ForeignKey("variable.id"), primary_key=True)
    items: Mapped[dict] = mapped_column(JSON, default=[])
