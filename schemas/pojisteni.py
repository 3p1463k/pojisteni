from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PojisteniBase(BaseModel):

    """Spolecne atributy"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    cena: Optional[int] = None
    datum_zalozeni: Optional[date] = datetime.now().date()


class VytvorPojisteni(PojisteniBase):

    """Atributy k validaci  pojisteni"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    cena: Optional[int] = None


class ZobrazPojisteni(PojisteniBase):

    """Zobrazeni pojisteni bez duvernych udaju"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    cena: Optional[int] = None
    owner_id: Optional[int] = None
    id: int = None

    datum_zalozeni: Optional[date]

    class Config:
        orm_mode = True


class UpravPojisteni(BaseModel):

    """Spolecne atributy"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    cena: Optional[int] = None
    datum_zalozeni: Optional[date]

    class Config:
        orm_mode = True
