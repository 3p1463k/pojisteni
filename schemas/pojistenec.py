from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from sqlmodel import Field
from sqlmodel import SQLModel

from db.models.pojistenec import Pojistenec
from db.models.pojistenec import PojistenecBase


class VytvorPojistence(SQLModel):

    """Atributy k validaci vytvoreni  pojistence"""

    jmeno: Optional[str] = Field(index=True)
    prijmeni: Optional[str] = Field(default=None)
    ulice: Optional[str] = Field(default=None)
    mesto: Optional[str] = Field(default=None)
    psc: Optional[int] = Field(default=None)
    telefon: Optional[int] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    password: Optional[str] = Field(default=None)


class ZobrazPojistence(SQLModel):

    """Zobrazeni pojistence bez hesla"""

    jmeno: str
    prijmeni: str
    ulice: str
    mesto: str
    psc: int
    telefon: int
    email: str
    id: int


class UpravPojistence(SQLModel):

    """Schema pro upravu pojistence"""

    jmeno: Optional[str] = Field(index=True)
    prijmeni: Optional[str] = Field(default=None)
    ulice: Optional[str] = Field(default=None)
    mesto: Optional[str] = Field(default=None)
    psc: Optional[int] = Field(default=None)
    telefon: Optional[int] = Field(default=None)
    email: Optional[str] = Field(default=None)
