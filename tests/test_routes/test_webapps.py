from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200


def test_about_page():
    response = client.get("/about/")
    assert response.status_code == 200


def test_login_page():
    response = client.get("/login/")
    assert response.status_code == 200


def test_registrace_page():
    response = client.get("/registr/")
    assert response.status_code == 200


def test_kontakt_page():
    response = client.get("/kontakt/")
    assert response.status_code == 200


def test_admin_page():
    response = client.get("/admin/")
    assert response.status_code == 200
