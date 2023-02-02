from typing import List
from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

from db.models.pojisteni import Pojisteni
from db.models.pojisteni import PojisteniBase


class VytvorPojisteni(PojisteniBase):

    """Atributy k validaci  pojisteni"""

    pass


class ZobrazPojisteni(Pojisteni):

    """Zobrazeni pojisteni bez duvernych udaju"""

    pass


class UpravPojisteni(SQLModel):

    """Schema pro upravu pojisteni"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)
