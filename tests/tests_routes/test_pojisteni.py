# import json
#
# from fastapi import status
#
#
# def test_vytvor_pojisteni(client):
#
#     """Test na vytvoreni pojisteni"""
#
#     data = {
#         "nazev": "Pojisteni auta",
#         "popis": "Havarijni pojisteni auta",
#         "cena": 1500,
#         "pojistenec_id": 1
#
#     }
#
#     response = client.post(
#         "/pojisteni/vytvor/",
#         json=data,
#     )
#
#     assert response.status_code == 200
#
#
# def test_zobraz_pojisteni(client):
#
#     data = {
#         "nazev": "Pojisteni zahrady",
#         "popis": "Pojistuje zahradu a plot",
#         "cena": 1500,
#         "pojistenec_id": 1
#     }
#
#     response = client.post(
#         "/pojisteni/vytvor/",
#         json=data,
#     )
#
#     response = client.get("/pojisteni/1")
#
#     assert response.status_code == 200
#
#
# def test_zobraz_vse_pojisteni(client):
#
#     """Zobrazi vse pojisteni"""
#
#     data = {"nazev": "Havarijni pojisteni", "popis": "Pojistuje auto", "cena": 1500}
#
#     client.post(
#         "/pojisteni/vytvor/",
#         json=data,
#     )
#
#     client.post(
#         "/pojisteni/vytvor/",
#         json=data,
#     )
#
#     response = client.get("/pojisteni/vse/")
#
#     assert response.status_code == 200
#     assert response.json()[0]
#     assert response.json()[1]
#
#
# def test_uprava_pojisteni(client):
#
#     """Jeno admin muze upravit, takze ocekavame HTTP_401_UNAUTHORIZED"""
#
#     data = {
#         "nazev": "Havarijni pojisteni EXTRA",
#         "popis": "Pojistuje auto",
#         "cena": 1500,
#         "datum_zalozeni": "2023-01-03",
#     }
#
#     client.post(
#         "/pojisteni/vytvor/",
#         json=data,
#     )
#
#     data["nazev"] = "Test novy nazev"
#
#     response = client.patch(
#         "/pojisteni/uprava/1",
#         json=data,
#     )
#
#     assert response.status_code == 200
#
#
# def test_vymaz_pojisteni(client):
#
#     """Vymaze pojisteni dle id"""
#
#     data = {"nazev": "Havarijni pojisteni", "popis": "Pojistuje auto", "cena": 1500}
#
#     client.post(
#         "/pojisteni/vytvor/",
#         json=data,
#     )
#
#     msg = client.delete("/pojisteni/vymazat/1")
#     response = client.get("/pojisteni/1")
#
#     assert response.status_code == status.HTTP_404_NOT_FOUND
