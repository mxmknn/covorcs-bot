"""Offline tests; fixtures describe no real coworking place."""

import socket

import pytest


@pytest.fixture(autouse=True)
def offline_network(monkeypatch):
    def denied(*args, **kwargs):
        raise AssertionError("network disabled in offline tests")

    monkeypatch.setattr(socket, "getaddrinfo", denied)
    monkeypatch.setattr(socket, "gethostbyname", denied)
    monkeypatch.setattr(socket, "gethostbyname_ex", denied)
    monkeypatch.setattr(socket, "gethostbyaddr", denied)
    for name in ("connect", "connect_ex", "sendto"):
        original = getattr(socket.socket, name)

        def guarded(self, *args, _original=original, **kwargs):
            if self.family != socket.AF_UNIX:
                return denied()
            return _original(self, *args, **kwargs)

        monkeypatch.setattr(socket.socket, name, guarded)


@pytest.fixture
def synthetic_record():
    from coworking_nearby.models import Coworking

    return Coworking("synthetic-001", "SYNTHETIC", "Test city, Example 1", 0, 0)
