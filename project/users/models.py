from sqlalchemy import Column, String, Integer
from project.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)

    def __int__(self, username, email, *args, **kwargs):
        self.username = username
        self.email = email

