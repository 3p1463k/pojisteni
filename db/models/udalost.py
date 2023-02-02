from datetime import date
from datetime import datetime
from typing import List
from typing import Optional

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


class UdalostBase(SQLModel):

    """Spolecne atributy"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    skoda: Optional[int] = Field(default=None)
    datum_zalozeni: Optional[date] = datetime.now().date()

    pojistenec_id: Optional[int] = Field(default=None, foreign_key="pojistenec.id")

    def __repr__(self):

        return f"{self.nazev }"


class Udalost(UdalostBase, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    pojistenec: "Pojistenec" = Relationship(back_populates="udalost")

    def __repr__(self):

        return f"{self.nazev }"
