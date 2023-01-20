from typing import List
from typing import Optional

from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):

        """TODO............"""

        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):

        """TODO..........."""

        form = await self.request.form()

        self.username = form.get("email")
        self.password = form.get("password")

        print(f"{self.username}")

    async def is_valid(self):

        """TODO................."""

        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")

        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")

        if not self.errors:

            return True

        return False


class RegistraceForm:
    def __init__(self, request: Request):

        """TODO............"""

        self.request: Request = request
        self.errors: List = []

        self.jmeno: Optional[str] = None
        self.prijmeni: Optional[str] = None
        self.ulice: Optional[str] = None
        self.mesto: Optional[str] = None
        self.psc: Optional[int] = None
        self.telefon: Optional[int] = None
        self.email: Optional[EmailStr] = None
        self.password: Optional[str] = None

    async def load_data(self):

        """TODO..........."""

        form = await self.request.form()

        self.jmeno = form.get("jmeno")
        self.prijmeni = form.get("prijmeni")
        self.ulice = form.get("ulice")
        self.mesto = form.get("mesto")
        self.psc = form.get("psc")
        self.telefon = form.get("telefon")
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):

        """TODO................."""

        if not self.jmeno or not (self.email.__contains__("@")):
            self.errors.append("Email is required")

        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")

        if not self.errors:

            return True

        return False


class PojisteniForm:
    def __init__(self, request: Request):

        """TODO............"""

        self.request: Request = request
        self.errors: List = []
        self.nazev: Optional[str] = None
        self.popis: Optional[str] = None
        self.cena: Optional[int] = None

    async def load_data(self):

        """TODO..........."""

        form = await self.request.form()

        self.nazev = form.get("nazev")
        self.popis = form.get("popis")
        self.cena = form.get("cena")

        # print(f"PRINTED FORM forms.py  {self.__dict__}")

    async def is_valid(self):

        """TODO................."""

        if not self.nazev:
            self.errors.append("Nazev is required")

        if self.nazev == "Vyberte pojisteni":
            self.errors.append("Vyberte pojisteni")

        # if not self.popis:
        #    self.errors.append("Popis is required")

        if not self.errors:

            return True

        return False


class UdalostForm:
    def __init__(self, request: Request):

        """TODO............"""

        self.request: Request = request
        self.errors: List = []
        self.nazev: Optional[str] = None
        self.popis: Optional[str] = None
        self.skoda: Optional[int] = None

    async def load_data(self):

        """TODO..........."""

        form = await self.request.form()

        self.nazev = form.get("nazev")
        self.popis = form.get("popis")
        self.skoda = form.get("skoda")

        # print(f"{self.__dict__}")

    async def is_valid(self):

        """TODO................."""

        if not self.nazev:
            self.errors.append("Nazev is required")

        if not self.popis or not len(self.popis) >= 5:
            self.errors.append("A valid popis is required")

        if not self.errors:

            return True

        return False


class AdminForm:
    def __init__(self):

        """TODO............"""

        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None
