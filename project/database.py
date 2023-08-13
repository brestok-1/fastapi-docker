from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from project.config import setting

Base = declarative_base()

engine = create_engine(
    setting.DATABASE_URL, connect_args=setting.DATABASE_CONNECT_DICT
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
