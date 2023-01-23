from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.repository.pojistenec import najdi_pojistence_dle_emailu
from db.repository.pojistenec import vytvor_noveho_pojistence
from schemas.pojistenec import VytvorPojistence


def user_authentication_headers(client: TestClient, email: str, password: str):

    """TODO.............."""

    data = {"username": email, "password": password}
    print(data)
    r = client.post("/login/token/", data=data)
    response = r.json()
    print(response)
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):

    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """

    password = "random-passW0rd"
    pojistenec = najdi_pojistence_dle_emailu(email=email, db=db)

    if not pojistenec:

        pojistenec_in_create = VytvorPojistence(
            jmeno="Janek",
            prijmeni="Dobrak",
            ulice="Nejaka 55",
            mesto="Paka",
            psc=20315,
            telefon=55555555,
            email="test@example.com",
            password="random-passW0rd",
        )

        pojistenec = vytvor_noveho_pojistence(pojistenec=pojistenec_in_create, db=db)

        return user_authentication_headers(
            client=client,
            email=email,
            password=password,
        )
