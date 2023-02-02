from fastapi import Request
from fastapi import Response
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from apis.version1.routes.route_login import get_current_user_from_token
from apis.version1.routes.route_login import login_for_access_token
from core.config import settings
from db.models.druh_pojisteni import DruhPojisteni
from db.models.pojistenec import Pojistenec
from db.repository.admin import vytvor_admina
from db.repository.druh_pojisteni import create_druh_pojisteni
from db.repository.pojistenec import create_pojistenec
from db.repository.pojistenec import find_pojistenec
from db.session import engine
from schemas.pojistenec import UpravPojistence
from schemas.pojistenec import VytvorPojistence
from schemas.pojistenec import ZobrazPojistence
from static.data.pojistenci1 import list_pojistencu
from static.data.pojistky import list_pojistek


def zadej_admina():

    print(f"\n Vytvarim admin ucet \n")

    with Session(engine) as session:

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

        admin_exixts = find_pojistenec(session, pojistenec_id=1)

        if admin_exixts:
            print(f"\n Polozka jiz existije: {admin_exixts.email}")
            pass

        else:
            pojistenec = vytvor_admina(pojistenec=pojistenec, session=session)


def vytvor_dummy_pojistence():

    """Vtvorime fiktivni pojistence do databaze"""

    for x in list_pojistencu:

        try:

            with Session(engine) as session:

                pojistenec_exists = (
                    session.query(Pojistenec)
                    .filter(Pojistenec.jmeno == x.jmeno)
                    .first()
                )

                if pojistenec_exists:

                    print(
                        f"Polozka jiz existije  {pojistenec_exists.jmeno} {pojistenec_exists.prijmeni}"
                    )
                    pass

                else:
                    pojistenec = create_pojistenec(session, x)

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

            with Session(engine) as session:

                if (
                    session.query(DruhPojisteni)
                    .filter(DruhPojisteni.nazev == x.nazev)
                    .first()
                ):

                    print(f"\n {x.nazev} jiz existuje")

                    pass

                else:

                    pojisteni = create_druh_pojisteni(session, x)

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

    with Session(engine) as session:

        pojistenec = (
            session.query(Pojistenec).filter(Pojistenec.email == username).first()
        )

        if pojistenec and pojistenec.is_superuser:
            # print(f"{pojistenec} is ADMIN")
            response = Response()
            res = login_for_access_token(
                response=response, form_data=myform, db=SessionLocal()
            )
