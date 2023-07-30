import datetime

from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    Enum,
    Integer,
    String,
    JSON,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.domains import VariableConstraintEnum, VariableRangeEnum


class Formula(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(32), nullable=False)
    created = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.datetime.now, nullable=False)
    tree = Column(JSON, nullable=False, default={})

    variables = relationship("Variable", back_populates="formula_id")


class Variable(Base):
    id = Column(BigInteger, primary_key=True)
    formula_id = Column(Integer, ForeignKey("formula.id"), index=True)
    name = Column(String(16), nullable=False)
    description = Column(Text)
    default = Column(Text)
    constraint_type = Column(Enum(VariableConstraintEnum))


class VariableRangeConstraint(Base):
    id = Column(BigInteger, ForeignKey("variable.id"), primary_key=True)
    type = Column(Enum(VariableRangeEnum), nullable=False)
