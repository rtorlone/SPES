from enum import Enum

from pycountry import countries
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum
from sqlalchemy.orm import relationship, backref

from database.database import Base

alpha3_codes = [country.alpha_3 for country in list(countries)]


class PersonCitizenship(Base):
    """
    Questa classe definisce la cittadinanza della Persona Fragile
    """
    __tablename__ = "person_citizenship"
    id = Column(String, primary_key=True, index=True)
    created_by = Column(String,  ForeignKey("user.id"), nullable=False) #foreign key to creator user
    owner_id = Column(String, ForeignKey("user.id"), nullable=False) #foreign key to owner user
    pf_id = Column(String, ForeignKey("person.id"), nullable=False)  # foreign key to owner user
    nation_id = Column(Enum(*alpha3_codes, name="alpha3_codes"), nullable=False)
    from_date = Column(Date, nullable=False)  # è una data
    created = Column(Date) # è una data
    updated = Column(Date) # è una data

    creator = relationship("User", foreign_keys=[created_by], uselist=False)
    owner = relationship("User",  foreign_keys=[owner_id], uselist=False)
    pf = relationship("Person", foreign_keys=[pf_id])