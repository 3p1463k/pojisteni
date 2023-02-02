from datetime import date
from datetime import datetime
from typing import List
from typing import Optional

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


class DruhPojisteniBase(SQLModel):

    """Spolecne atributy"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)


class DruhPojisteni(DruhPojisteniBase, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
