from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app._core.config import settings


engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
