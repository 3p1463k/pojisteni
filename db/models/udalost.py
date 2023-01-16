from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Udalost(Base):

    """Vytvorime model pojistence"""

    id = Column(Integer, primary_key=True, index=True)

    nazev = Column(String, nullable=False)
    popis = Column(String, nullable=False)
    skoda = Column(Integer, nullable=False)
    datum_zalozeni = Column(Date)

    owner_id = Column(Integer, ForeignKey("pojistenec.id"))
    owner = relationship("Pojistenec", back_populates="udalost")

    def __repr__(self):

        return self.nazev
