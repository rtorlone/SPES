from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum
from sqlalchemy.orm import relationship, backref

from database.database import Base


class Permission(Base):
    """
    Questa classe definisce i permessi di ciascun utente per uno specifico documento.
    """
    __tablename__ = "permission"
    user_id = Column(String, ForeignKey("user.id"), primary_key=True, index=True)
    document_id = Column(String, ForeignKey("person_report.id"), primary_key=True, index=True)
    permission = Column(Boolean, default=False)
    created = Column(Date, nullable=False)
    pending = Column(Boolean, default=True)

    user = relationship("User", foreign_keys=[user_id], uselist=False)
    document = relationship("PersonReport", foreign_keys=[document_id], uselist=False)
