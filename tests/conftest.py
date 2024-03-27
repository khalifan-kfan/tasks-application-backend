import pytest
from starlette.testclient import TestClient
from pytest import fixture
from starlette.config import environ

from main import app


fixture(scope="module")


def test_app():
    client = TestClient(app)
    with client:
        yield client


@fixture(scope="session")
def test_client():
    with TestClient(app) as test_client:
        yield test_client


environ['TESTING'] = 'TRUE'
