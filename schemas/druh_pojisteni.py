from typing import List
from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

from db.models.druh_pojisteni import DruhPojisteni
from db.models.druh_pojisteni import DruhPojisteniBase


class VytvorDruhPojisteni(SQLModel):

    """Atributy k validaci  pojisteni"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)


class ZobrazDruhPojisteni(DruhPojisteni):

    """Zobrazeni pojisteni bez citlivych udaju"""

    pass


class UpravDruhPojisteni(SQLModel):

    """Schema pro upravu pojisteni"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)
