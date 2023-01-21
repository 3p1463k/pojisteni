from fastapi import Request
from fastapi import Response
from sqlalchemy.exc import IntegrityError

from apis.version1.routes.route_login import get_current_user_from_token
from apis.version1.routes.route_login import login_for_access_token
from core.config import settings
from db.models.druh_pojisteni import DruhPojisteni
from db.models.pojistenec import Pojistenec
from db.repository.admin import vytvor_admina
from db.repository.druh_pojisteni import vytvor_novy_druh_pojisteni
from db.repository.pojistenec import vytvor_noveho_pojistence
from db.session import SessionLocal
from schemas.pojistenec import UpravPojistence
from schemas.pojistenec import VytvorPojistence
from schemas.pojistenec import ZobrazPojistence
from static.data.pojistenci1 import list_pojistencu
from static.data.pojistky import list_pojistek


def zadej_admina():

    print(f"\n Vytvarim admin ucet \n")

    with SessionLocal() as session:

        pojistenec = VytvorPojistence(
            jmeno="Bohousek",
            prijmeni="Admin",
            ulice="Strasna 8",
            mesto="Hrosice",
            psc=15478,
            telefon=5894562,
            email="bohousek@admin.com",
            password="adminheslo",
        )

        try:
            pojistenec = vytvor_admina(pojistenec=pojistenec, db=SessionLocal())

        except IntegrityError as e:
            print(f"Polozka jiz existije \n {e.params[0:2]}")
            pass


def vytvor_dummy_pojistence():

    """Vtvorime fiktivni pojistence do databaze"""

    for x in list_pojistencu:

        try:
            pojistenec = vytvor_noveho_pojistence(x, db=SessionLocal())

            print(
                f"Vytvarim fiktivni pojistence {pojistenec.jmeno} {pojistenec.prijmeni}"
            )

        except IntegrityError as e:
            print(f"Polozka jiz existije  {e.params[0:2]}")
            pass


def vytvor_dummy_pojisteni():

    """Vtvorime fiktivni pojisteni do databaze"""

    for x in list_pojistek:

        try:

            with SessionLocal() as session:

                if (
                    session.query(DruhPojisteni)
                    .filter(DruhPojisteni.nazev == x.nazev)
                    .first()
                ):

                    print(f"{x.nazev} jiz existuje")

                    pass

                else:

                    pojisteni = vytvor_novy_druh_pojisteni(
                        x,
                        db=SessionLocal(),
                    )

                    print(f"Vytvarim fiktivni pojisteni {pojisteni.nazev}")

        except IntegrityError as e:
            print(f"Polozka jiz existije  {e.params}")
            pass


def over_admina():

    """Token pro  admina"""

    class MyForm:
        def __init__(self, username, password):
            self.username = username
            self.password = password

    username = "bohousek@admin.com"
    password = "adminheslo"
    myform = MyForm(username, password)

    print(f"\n Prihlasuji admina pro vytvoreni polozek \n")

    with SessionLocal() as session:

        pojistenec = (
            session.query(Pojistenec).filter(Pojistenec.email == username).first()
        )

        if pojistenec and pojistenec.is_superuser:
            # print(f"{pojistenec} is ADMIN")
            response = Response()
            res = login_for_access_token(
                response=response, form_data=myform, db=SessionLocal()
            )
