from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database.database import Base

class PersonReport(Base):
    """
    Questa classe definisce un referto medico relativo ad una Persona Fragile
    """

    __tablename__ = "person_report"
    id = Column(String, primary_key=True, index=True)
    pf_id = Column(String, ForeignKey("person.id"), index=True, nullable=False)
    title = Column(String, nullable=False)
    upload_date = Column(Date, nullable=False)
    path = Column(String, nullable=False)
    upload_by = Column(String, ForeignKey("user.id"), nullable=False)

    person = relationship("Person", foreign_keys=[pf_id], uselist=False)
    uploader = relationship("User", foreign_keys=[upload_by], uselist=False)

    permissions = relationship("Permission", back_populates="document", uselist=True)


