import json

from fastapi import status


def test_vytvor_pojistence(client, normal_user_token_headers):

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
    print(data)

    response = client.post(
        "/pojistenci/vytvorit/",
        json=data,
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200

    assert response.json() == {
        "jmeno": "Brona",
        "prijmeni": "Hanzak",
        "ulice": "Vyjezdni 25",
        "mesto": "Nova Paka",
        "psc": 255489,
        "telefon": 589657123,
        "email": "bohous@testinexampl.com",
        "password": None,
        "is_active": True,
    }


def test_zobraz_pojistence(client, normal_user_token_headers):

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

    response = client.get("/pojistenci/1")

    assert response.status_code == 200


def test_zobraz_vsechny_pojistence(client, normal_user_token_headers):

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
        "/pojistenci/vytvorit/",
        json=data,
        headers=normal_user_token_headers,
    )

    client.post(
        "/pojistenci/vytvorit/",
        json=data1,
        headers=normal_user_token_headers,
    )

    response = client.get("/pojistenci/vse/")

    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_uprava_pojistence(client, normal_user_token_headers):

    """Vytvorime pojistence a nasledovne upravime jmeno"""

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
        "/pojistenci/vytvorit/",
        json=data,
        headers=normal_user_token_headers,
    )

    data["jmeno"] = "Nove Jmeno"
    del data["password"]

    response = client.put(
        "/pojistenci/uprava/2",
        json=data,
        headers=normal_user_token_headers,
    )

    assert response.json()["msg"] == "Successfully updated data."


def test_vymaz_pojistence(client, normal_user_token_headers):

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
        "/pojistenci/vytvorit/",
        json=data,
        headers=normal_user_token_headers,
    )

    msg = client.delete("/pojistenci/vymazat/2")
    response = client.get("/pojistenci/2")

    assert response.status_code == status.HTTP_404_NOT_FOUND
