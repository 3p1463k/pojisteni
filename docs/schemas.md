# Schemas

## Pojistenec

### VytvorPojistence
```py
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
```
### ZobrazPojistence
```py
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
```
### UpravPojistence
```py
class UpravPojistence(SQLModel):

    """Schema pro upravu pojistence"""

    jmeno: Optional[str] = Field(index=True)
    prijmeni: Optional[str] = Field(default=None)
    ulice: Optional[str] = Field(default=None)
    mesto: Optional[str] = Field(default=None)
    psc: Optional[int] = Field(default=None)
    telefon: Optional[int] = Field(default=None)
    email: Optional[str] = Field(default=None)
```
## Pojisteni

### VytvorPojisteni
```py
class VytvorPojisteni(PojisteniBase):

    """Atributy k validaci  pojisteni"""

    pass

```
### ZobrazPojisteni
```py
class ZobrazPojisteni(Pojisteni):

    """Zobrazeni pojisteni bez duvernych udaju"""

    pass
```
### UpravPojisteni
```py
class UpravPojisteni(SQLModel):

    """Schema pro upravu pojisteni"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)
```
## Udalosti

### VytvorUdalost
```py

class VytvorUdalost(UdalostBase):

    """Atributy k validaci  pojisteni"""

    pass
```
### ZobrazUdalost
```py
class ZobrazUdalost(Udalost):

    """Zobrazeni pojisteni bez duvernych udaju"""

    pass
```
### UpravUdalost
```py
class UpravUdalost(SQLModel):

    """Schema pro upravu pojisteni"""

    nazev: Optional[str] = Field(default=None)
    popis: Optional[str] = Field(default=None)
    cena: Optional[int] = Field(default=None)
```
## Token
### Token schema
```py
class Token(SQLModel):

    """Token schema"""

    access_token: str
    token_type: str
```
