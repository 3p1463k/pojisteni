# Models


## SQLModel database models

## Pojistenec

### PojistenecBase
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
### Pojistenec (table=True)

```py
class Pojistenec(PojistenecBase, table=True):

    """Model a relationship pro vytvoreni databaze"""

    id: Optional[int] = Field(default=None, primary_key=True)

    pojisteni: List["Pojisteni"] = Relationship(

        back_populates="pojistenec",
        sa_relationship_kwargs={"cascade": "delete"}
    )

    udalost: List["Udalost"] = Relationship(

        back_populates="pojistenec",
        sa_relationship_kwargs={"cascade": "delete"}
    )
```
## Pojisteni

### PojisteniBase
```py
class PojisteniBase(SQLModel):

    """Spolecne atributy"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)
    datum_zalozeni: Optional[date] = datetime.now().date()

    pojistenec_id: Optional[int] = Field(default=None, foreign_key="pojistenec.id")
```
### Pojisteni (table=True)
```py
class Pojisteni(PojisteniBase, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    pojistenec: Optional["Pojistenec"] = Relationship(back_populates="pojisteni")
```
## Udalosti

### UdalostBase
```py

class UdalostBase(SQLModel):

    """Spolecne atributy"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    skoda: Optional[int] = Field(default=None)
    datum_zalozeni: Optional[date] = datetime.now().date()

    pojistenec_id: Optional[int] = Field(default=None, foreign_key="pojistenec.id")

```
### Udalost (table=True )
```py
class Udalost(UdalostBase, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    pojistenec: "Pojistenec" = Relationship(back_populates="udalost")
```
