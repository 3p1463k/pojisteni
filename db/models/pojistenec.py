from datetime import date
from datetime import datetime
from typing import List
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


class PojistenecBase(SQLModel):

    """Base model"""

    jmeno: Optional[str] = Field(index=True)
    prijmeni: Optional[str] = Field(default=None)
    ulice: Optional[str] = Field(default=None)
    mesto: Optional[str] = Field(default=None)
    psc: Optional[int] = Field(default=None)
    telefon: Optional[int] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    hashed_password: Optional[str] = Field(default=None)

    is_active: Optional[bool] = Field(default=True)
    is_superuser: Optional[bool] = Field(default=False)

    def __repr__(self):

        return f"{self.jmeno}"


class Pojistenec(PojistenecBase, table=True):

    """Model a relationship pro vytvoreni databaze"""

    id: Optional[int] = Field(default=None, primary_key=True)

    pojisteni: List["Pojisteni"] = Relationship(
        back_populates="pojistenec", sa_relationship_kwargs={"cascade": "delete"}
    )

    udalost: List["Udalost"] = Relationship(
        back_populates="pojistenec", sa_relationship_kwargs={"cascade": "delete"}
    )

    def __repr__(self):

        return f"{self.jmeno}"


class PojistenecOut(SQLModel):

    """Zobrazeni bez hesla"""

    jmeno: str
    prijmeni: str
    email: str
