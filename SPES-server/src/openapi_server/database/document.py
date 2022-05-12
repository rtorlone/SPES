from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database.database import Base

class PersonDocument(Base):
    """
    Questa classe definisce un documento amministrativo relativo ad una Persona Fragile
    """

    __tablename__ = "person_document"
    id = Column(String, primary_key=True, index=True)
    pf_id = Column(String, ForeignKey("person.id"), index=True, nullable=False)
    upload_by = Column(String, ForeignKey("user.id"), nullable=False)
    tipologia = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    number = Column(String, nullable=True)
    place_of_issue = Column(String)
    release_date = Column(Date, nullable=False)
    upload_date = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=False)
    path = Column(String, nullable=False)

    person = relationship("Person", foreign_keys=[pf_id], uselist=False)
    uploader = relationship("User", foreign_keys=[upload_by], uselist=False)

