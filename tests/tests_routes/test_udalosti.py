import json

from fastapi import status


def test_vytvor_udalost(client, admin_token_headers):

    """Test na vytvoreni udalosti"""

    data = {
        "nazev": "Rozbite auto",
        "popis": "Tukli do me u Kauflandu",
        "skoda": 15000,
        "pojistenec_id": 1,
    }

    response = client.post(
        "/udalosti/vytvor/",
        json=data,
    )

    assert response.status_code == 200


def test_zobraz_udalost(client, admin_token_headers):

    """Zobrazi udalost"""

    data = {
        "nazev": "Rozbite auto",
        "popis": "Tukli do me u Kauflandu",
        "skoda": 15000,
        "owner_id": 2,
    }

    response = client.post(
        "/udalosti/vytvor/",
        json=data,
        headers=admin_token_headers,
    )

    response = client.get("/udalosti/1")

    assert response.status_code == 200


def test_zobraz_vse_udalosti(client, admin_token_headers):

    """Zobrazi vsechny udalosti"""

    data = {
        "nazev": "Rozbite auto",
        "popis": "Tukli do me u Kauflandu",
        "skoda": 15000,
        "owner_id": 2,
    }

    response = client.post(
        "/udalosti/vytvor/",
        json=data,
        headers=admin_token_headers,
    )

    data1 = {
        "nazev": "Rozbita motorka",
        "popis": "Tukli do me u Kauflandu",
        "skoda": 45000,
        "owner_id": 2,
    }

    response = client.post(
        "/udalosti/vytvor/",
        json=data1,
        headers=admin_token_headers,
    )

    response = client.get("/udalosti/vse/")

    assert response.status_code == 200
    assert response.json()[0]
    assert response.json()[1]


def test_uprav_udalost(client, admin_token_headers):

    """Uprava udalosti test"""

    data = {
        "nazev": "Rozbite auto",
        "popis": "Tukli do me u Kauflandu",
        "skoda": 15000,
        "owner_id": 2,
    }

    response = client.post(
        "/udalosti/vytvor/",
        json=data,
        headers=admin_token_headers,
    )

    data["nazev"] = "Test novy nazev"

    response = client.patch(
        "/udalosti/uprav/1",
        json=data,
        headers=admin_token_headers,
    )

    assert response.status_code == 200


def test_vymaz_udalost(client, admin_token_headers):

    """Vymaze udalost dle zadaneho id"""

    data = {
        "nazev": "Rozbite auto",
        "popis": "Tukli do me u Kauflandu",
        "skoda": 15000,
        "owner_id": 2,
    }

    response = client.post(
        "/udalosti/vytvor/",
        json=data,
        headers=admin_token_headers,
    )

    msg = client.delete("/udalost/vymazat/1")
    response = client.get("/udalost/1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
