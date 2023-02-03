# Models


## SQLModel database models

### Pojistenec

PojistenecBase
```py

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

```
Pojistenec table=True

```py
class Pojistenec(PojistenecBase, table=True):

    """Model a relationship pro vytvoreni databaze"""

    id: Optional[int] = Field(default=None, primary_key=True)

    pojisteni: List["Pojisteni"] = Relationship(
        back_populates="pojistenec", sa_relationship_kwargs={"cascade": "delete"}
    )

    udalost: List["Udalost"] = Relationship(
        back_populates="pojistenec", sa_relationship_kwargs={"cascade": "delete"}
    )
```

### Pojisteni
```py
class VytvorPojisteni(PojisteniBase):

    """Atributy k validaci  pojisteni"""

    pass


class ZobrazPojisteni(Pojisteni):

    """Zobrazeni pojisteni bez duvernych udaju"""

    pass


class UpravPojisteni(SQLModel):

    """Schema pro upravu pojisteni"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)
```
### Udalosti
```py

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
```
