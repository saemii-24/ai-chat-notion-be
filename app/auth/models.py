from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String(255), nullable=False)
