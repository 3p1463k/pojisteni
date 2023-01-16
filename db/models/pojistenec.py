from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Pojistenec(Base):

    """Vytvorime model pojistence"""

    id = Column(Integer, primary_key=True, index=True)

    jmeno = Column(String, nullable=False)
    prijmeni = Column(String, nullable=False)
    ulice = Column(String, nullable=False)
    mesto = Column(String, nullable=False)
    psc = Column(Integer, nullable=False)
    telefon = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)

    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    pojisteni = relationship("Pojisteni", back_populates="owner")
    udalost = relationship("Udalost", back_populates="owner")

    def __repr__(self):

        return f"{self.jmeno} {self.prijmeni}"
