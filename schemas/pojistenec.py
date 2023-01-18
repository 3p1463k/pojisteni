from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class PojistenecBase(BaseModel):

    """Base model"""

    jmeno: Optional[str] = None
    prijmeni: Optional[str] = None
    ulice: Optional[str] = None
    mesto: Optional[str] = None
    psc: Optional[int] = 0
    telefon: Optional[int] = 0
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class VytvorPojistence(PojistenecBase):

    """Atributy k vytvoreni  pojistence"""

    jmeno: str
    prijmeni: str
    ulice: str
    mesto: str
    psc: int
    telefon: int
    email: EmailStr
    password: str


class UpravPojistence(BaseModel):

    jmeno: Optional[str] = None
    prijmeni: Optional[str] = None
    ulice: Optional[str] = None
    mesto: Optional[str] = None
    psc: Optional[int] = 0
    telefon: Optional[int] = 0
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class ZobrazPojistence(PojistenecBase):

    """Zobrazeni pojistence bez duvernych udaju"""

    jmeno: str
    prijmeni: str
    ulice: str
    mesto: str
    psc: int
    telefon: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True