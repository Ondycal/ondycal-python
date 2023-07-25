from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Formula(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
