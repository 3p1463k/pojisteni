import json

from fastapi import status


def test_vytvor_pojistence(client, admin_token_headers):

    """Test na vytvoreni noveho pojistence"""

    data = {
        "jmeno": "Brona",
        "prijmeni": "Hanzak",
        "ulice": "Vyjezdni 25",
        "mesto": "Nova Paka",
        "psc": 255489,
        "telefon": 589657123,
        "email": "bohous@testinexampl.com",
        "password": "testovani",
    }

    response = client.post(
        "/pojistenec/vytvorit/",
        json=data,
    )

    assert response.status_code == 200

    assert response.json()["jmeno"] == "Brona"
    assert response.json()["prijmeni"] == "Hanzak"
    assert response.json()["email"] == "bohous@testinexampl.com"


def test_zobraz_pojistence(client, admin_token_headers):

    """TODO......."""

    data = {
        "jmeno": "Brona",
        "prijmeni": "Hanzak",
        "ulice": "Vyjezdni 25",
        "mesto": "Nova Paka",
        "psc": 255489,
        "telefon": 589657123,
        "email": "bohous@testinexampl.com",
        "password": "testovani",
    }

    client.post(
        "/pojistenec/vytvorit/",
        json=data,
    )

    response = client.get("/pojistenec/1")

    assert response.status_code == 200


def test_zobraz_vsechny_pojistence(client, admin_token_headers):

    """TODO......."""

    data = {
        "jmeno": "Brona",
        "prijmeni": "Hanzak",
        "ulice": "Vyjezdni 25",
        "mesto": "Nova Paka",
        "psc": 255489,
        "telefon": 589657123,
        "email": "bohous@testinexampl.com",
        "password": "testovani",
    }

    data1 = {
        "jmeno": "Brona1",
        "prijmeni": "Hanzak1",
        "ulice": "Vyjezdni 251",
        "mesto": "Nova Paka1",
        "psc": 255411,
        "telefon": 19657123,
        "email": "brona@test.com",
        "password": "testovani",
    }

    client.post(
        "/pojistenec/vytvorit/",
        json=data,
    )

    client.post(
        "/pojistenec/vytvorit/",
        json=data1,
    )

    response = client.get("/pojistenci/vse/")

    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_uprava_pojistence(client, admin_token_headers):

    """Uprava test"""

    data = {
        "jmeno": "Bohumil",
        "prijmeni": "Hanzak",
        "ulice": "Vyjezdni 25",
        "mesto": "Nova Paka",
        "psc": 255489,
        "telefon": 589657123,
        "email": "bohous@testil.com",
        "password": "testovani",
    }

    client.post(
        "/pojistenec/vytvorit/",
        json=data,
    )

    data["jmeno"] = "Nove Jmeno"
    del data["password"]
    # print(data)

    response = client.patch(
        "/pojistenec/uprava/1",
        json=data,
    )

    assert response.status_code == 200


def test_vymaz_pojistence(client, admin_token_headers):

    """Vytvorime pojistence a nasledovne zkusime vymazat"""

    data = {
        "jmeno": "Bohumil",
        "prijmeni": "Hanzak",
        "ulice": "Vyjezdni 25",
        "mesto": "Nova Paka",
        "psc": 255489,
        "telefon": 589657123,
        "email": "bohous@testinexampl.com",
        "password": "testovani",
    }

    client.post(
        "/pojistenec/vytvorit/",
        json=data,
    )

    msg = client.delete("/pojistenec/vymazat/1")
    response = client.get("/pojistenec/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
