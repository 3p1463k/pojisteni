from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UdalostBase(BaseModel):

    """Spolecne atributy"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    skoda: Optional[int] = None
    owner_id: Optional[int] = None
    datum_zalozeni: Optional[date] = datetime.now().date()


class VytvorUdalost(UdalostBase):

    """Atributy k validaci  pojisteni"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    skoda: Optional[int] = None
    owner_id: Optional[int] = None


class ZobrazUdalost(BaseModel):

    """Zobrazeni pojisteni bez duvernych udaju"""

    nazev: Optional[str] = None
    popis: Optional[str] = None
    skoda: Optional[int] = None
    owner_id: Optional[int] = None
    id: Optional[int] = None
    datum_zalozeni: Optional[date]

    class Config:
        orm_mode = True
