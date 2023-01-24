from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DruhPojisteniBase(BaseModel):

    """Spolecne atributy"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    cena: Optional[int] = None


class VytvorDruhPojisteni(DruhPojisteniBase):

    """Atributy k validaci  pojisteni"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    cena: Optional[int] = None


class ZobrazDruhPojisteni(BaseModel):

    """Zobrazeni pojisteni bez citlivych udaju"""

    nazev: str
    popis: str
    cena: int
    id: int

    class Config:
        orm_mode = True


class UpravDruhPojisteni(BaseModel):

    """Spolecne atributy"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    cena: Optional[int] = None

    class Config:
        orm_mode = True
