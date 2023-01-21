from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.base_class import Base


class DruhPojisteni(Base):

    """Vytvorime model druhu pojisteni"""

    id = Column(Integer, primary_key=True, index=True)

    nazev = Column(String, nullable=False)
    popis = Column(String, nullable=False)
    cena = Column(Integer, default=0)

    def __repr__(self):

        return f"{self.nazev }"
