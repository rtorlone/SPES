from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum
from sqlalchemy.orm import relationship

from database.database import Base


class User(Base):
    """
    Questa classe definisce le credenziali di accesso dell'utente.
    """
    __tablename__ = "user"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, nullable=True)
    pwd = Column(String)
    role = Column(String, default=False)
    first_access = Column(Boolean, default=True)


