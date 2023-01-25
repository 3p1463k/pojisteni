import json

from fastapi import status


def test_vytvor_pojisteni(client, normal_user_token_headers):

    """Test na vytvoreni pojisteni"""

    data = {
        "nazev": "Pojisteni auta",
        "popis": "Havarijni pojisteni auta",
        "cena": 1500,
    }

    response = client.post(
        "/pojisteni/zaloz/",
        json=data,
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200


def test_zobraz_pojisteni(client, normal_user_token_headers):

    data = {
        "nazev": "Pojisteni zahrady",
        "popis": "Pojistuje zahradu a plot",
        "cena": 1500,
    }

    response = client.post(
        "/pojisteni/zaloz/",
        json=data,
        headers=normal_user_token_headers,
    )

    response = client.get("/pojisteni/1")

    assert response.status_code == 200


def test_zobraz_vse_pojisteni(client, normal_user_token_headers):

    """Zobrazi vse pojisteni"""

    data = {"nazev": "Havarijni pojisteni", "popis": "Pojistuje auto", "cena": 1500}

    client.post(
        "/pojisteni/zaloz/",
        json=data,
        headers=normal_user_token_headers,
    )

    client.post(
        "/pojisteni/zaloz/",
        json=data,
        headers=normal_user_token_headers,
    )

    response = client.get("/pojisteni/vse/")

    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_uprava_pojisteni(client, normal_user_token_headers):

    """Jeno admin muze upravit, takze ocekavame HTTP_401_UNAUTHORIZED"""

    data = {
        "nazev": "Havarijni pojisteni EXTRA",
        "popis": "Pojistuje auto",
        "cena": 1500,
        "datum_zalozeni": "2023-01-03",
    }

    client.post(
        "/pojisteni/zaloz/",
        json=data,
        headers=normal_user_token_headers,
    )

    data["nazev"] = "Test novy nazev"

    response = client.put(
        "/pojisteni/uprava/1",
        json=data,
        headers=normal_user_token_headers,
    )

    assert response.status_code == 401


def test_vymaz_pojisteni(client, normal_user_token_headers):

    """Vymaze pojisteni dle id"""

    data = {"nazev": "Havarijni pojisteni", "popis": "Pojistuje auto", "cena": 1500}

    client.post(
        "/pojisteni/vytvor/",
        json=data,
        headers=normal_user_token_headers,
    )

    msg = client.delete("/pojisteni/vymazat/1")
    response = client.get("/pojisteni/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
