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


class ZobrazDruhPojisteni(DruhPojisteniBase):

    """Zobrazeni pojisteni bez duvernych udaju"""

    nazev: str
    popis: str
    cena: int

    class Config:
        orm_mode = True


class UpravDruhPojisteni(BaseModel):

    """Spolecne atributy"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    cena: Optional[int] = None
    datum_zalozeni: Optional[date]

    class Config:
        orm_mode = True
