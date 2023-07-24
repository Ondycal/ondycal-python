from sqlalchemy import Column, Integer

from app.db.init_db import Base


class Formula(Base):
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True, index=True)
