from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum
from sqlalchemy.orm import relationship, backref

from database.database import Base


class PersonMaritalStatus(Base):
    """
    Questa classe definisce il marital status della persona fragile.
    """
    __tablename__ = "person_marital_status"
    id = Column(String, primary_key=True, index=True)
    created_by = Column(String, ForeignKey("user.id"), nullable=False)  # foreign key to creator user
    owner_id = Column(String, ForeignKey("user.id"), nullable=False)  # foreign key to owner user
    pf_id = Column(String, ForeignKey("person.id"), nullable=False)  # foreign key to owner user
    marital_status_code = Column(Enum("COH", "DIV", "LSE", "MAR", "SIN", "WID", name="marital_status_codes"), nullable=False)
    from_date = Column(Date, nullable=False)  # è una data
    created = Column(Date)  # è una data
    updated = Column(Date)  # è una data

    creator = relationship("User", foreign_keys=[created_by], uselist=False)
    owner = relationship("User", foreign_keys=[owner_id], uselist=False)
    pf = relationship("Person", foreign_keys=[pf_id])
