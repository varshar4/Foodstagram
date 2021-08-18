from test import client


def test_landing(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert landing.status_code == 200


def test_landing_aliases(client):
    landing = client.get("/")
    assert client.get("/").data == landing.data