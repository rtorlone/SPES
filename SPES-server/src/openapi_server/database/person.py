from pycountry import countries
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum, CheckConstraint
from sqlalchemy.orm import relationship, backref

from database.database import Base

alpha3_codes = [country.alpha_3 for country in list(countries)]


class Person(Base):
    """
    Questa classe definisce la Persona Fragile (PF)
    """
    __tablename__ = "person"

    id = Column(String, primary_key=True, index=True)
    created_by = Column(String, ForeignKey("user.id"))  # foreign key to creator user
    owner_id = Column(String, ForeignKey("user.id"))  # foreign key to owner user
    user_id = Column(String, ForeignKey("user.id"))  # foreign key to owner user
    is_dead = Column(Boolean, default=False)
    death_date = Column(Date)
    cf = Column(String(length=16), index=True)
    cui_code = Column(String, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    fullname = Column(String, index=True)
    nicknames = Column(String, index=True)
    gender = Column(Enum("M", "F", name="gender"), index=True)
    birth_date = Column(Date, index=True)
    verified = Column(Boolean, default=False)
    created = Column(Date)  # è una data
    updated = Column(Date)  # è una data
    sanitary_district_id = Column(String)
    # updated_by = Column(String, index=True, ForeignKey("table.id"))  # foreign key to the last user to update
    is_anonymous = Column(Boolean, default=False)
    is_foreign = Column(Boolean, default=False)
    birth_city = Column(String)
    birth_geoarea_id = Column(String, index=True)
    birth_nation_id = Column(Enum(*alpha3_codes, name="alpha3_codes"), index=True)

    creator = relationship("User", foreign_keys=[created_by])
    owner = relationship("User", foreign_keys=[owner_id], uselist=False)
    user = relationship("User", foreign_keys=[user_id])

    addresses = relationship("PersonAddress", back_populates="pf", uselist=True)
    citizenships = relationship("PersonCitizenship", back_populates="pf", uselist=True)
    marital_status = relationship("PersonMaritalStatus", back_populates="pf", uselist=True)
