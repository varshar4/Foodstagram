from test import client


def test_landing(client):
    landing = client.get("/")

    assert landing.status_code == 200
