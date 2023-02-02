from typing import List
from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel

from db.models.udalost import Udalost
from db.models.udalost import UdalostBase


class VytvorUdalost(UdalostBase):

    """Atributy k validaci  pojisteni"""

    pass


class ZobrazUdalost(Udalost):

    """Zobrazeni pojisteni bez duvernych udaju"""

    pass


class UpravUdalost(SQLModel):

    """Schema pro upravu pojisteni"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)
