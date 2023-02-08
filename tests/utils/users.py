from fastapi.testclient import TestClient
from sqlmodel import Session

from db.repository.login import najdi_pojistence_dle_emailu
from db.repository.pojistenec import create_pojistenec
from schemas.pojistenec import VytvorPojistence


def user_authentication_headers(client, email: str, password: str):

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


def authentication_token_from_email(session, client, email: str, password: str):
    """Return a token with given email"""

    return user_authentication_headers(client, email, password)
