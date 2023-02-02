from fastapi.testclient import TestClient
from sqlmodel import Session

from db.repository.login import najdi_pojistence_dle_emailu
from db.repository.pojistenec import create_pojistenec
from schemas.pojistenec import VytvorPojistence


def user_authentication_headers(client: TestClient, email: str, password: str):

    """TODO.............."""

    data = {"username": email, "password": password}
    # print(data)
    r = client.post("/login/token/", data=data)
    print(r)
    response = r.json()
    print(response)
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}

    return headers


def authentication_token_from_email(client: TestClient, email: str, session: Session):

    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """

    password = "random-passW0rd"
    pojistenec = najdi_pojistence_dle_emailu(email, session)

    if not pojistenec:

        pojistenec = VytvorPojistence(
            jmeno="Janek",
            prijmeni="Dobrak",
            ulice="Nejaka 55",
            mesto="Paka",
            psc=20315,
            telefon=55555555,
            email="test@example.com",
            password="random-passW0rd",
        )

        pojistenec = create_pojistenec(session, pojistenec)
        print(pojistenec)

    return user_authentication_headers(client=client, email=email, password=password)
