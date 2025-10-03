import pytest
from pyserveuz.app import PyServeApp


@pytest.fixture
def app():
    return PyServeApp()


@pytest.fixture
def test_client(app):
    return app.test_session()