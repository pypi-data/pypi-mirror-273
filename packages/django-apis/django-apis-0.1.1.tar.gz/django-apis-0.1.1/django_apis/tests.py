from django.test import TestCase
from .response import SimpleJsonResponsePackage


class TestDjangoApis(TestCase):

    def test1(self):
        response = SimpleJsonResponsePackage("pong", None)
        data = response.pack()
        assert data
        assert data["data"] == "pong"

    def test2(self):
        response = SimpleJsonResponsePackage(None, RuntimeError(1, "info"))
        data = response.pack()
        assert data
        assert data["data"] is None
        assert data["success"] is False
        assert data["code"] == 1
        assert data["msg"] == "info"
