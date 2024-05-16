from django.test import TestCase
from django.test import LiveServerTestCase
from django.test import Client


class TestDjangoApisDebug(LiveServerTestCase):
    def test1(self):
        client = Client()
        response = client.get("/debug/ping")
        response_data = response.json()
        assert response_data["data"] == "pong"

    def test2(self):
        client = Client()
        response = client.get("/debug/echo")
        response_data = response.json()
        assert response_data["data"] is None
        assert response_data["success"] is False

    def test3(self):
        client = Client()
        response = client.post("/debug/echo")
        response_data = response.json()
        assert response_data["data"] is None
        assert response_data["success"] is False

    def test4(self):
        client = Client()
        response = client.post(
            "/debug/echo",
            data={
                "msg": "hello",
            },
            content_type="application/json",
        )
        response_data = response.json()
        assert response_data["data"] == "hello"
        assert response_data["success"]

    def test5(self):
        client = Client()
        response = client.post(
            "/debug/echo",
            data={
                "msg": "12345678901234567",
            },
            content_type="application/json",
        )
        response_data = response.json()
        assert response_data["data"] is None
        assert response_data["success"] is False

    def test6(self):
        client = Client()
        response = client.get("/debug/getRequestInfo")
        response_data = response.json()
        assert response_data["data"]
        assert response_data["success"]
