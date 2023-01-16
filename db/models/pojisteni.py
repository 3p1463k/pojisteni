from db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Pojisteni(Base):
    
    """Vytvorime model pojisteni"""
    
    id = Column(Integer,primary_key = True, index = True)
    
    nazev = Column(String,nullable = False)
    popis = Column(String,nullable = False)
    cena = Column(Integer ,default = 0)  
    datum_zalozeni = Column(Date)

    owner_id = Column(Integer, ForeignKey("pojistenec.id"))
    owner = relationship("Pojistenec", back_populates="pojisteni")

    def __repr__(self):       
         
         return self.nazev 
