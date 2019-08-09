import pytest

from dearkids import app as app_


@pytest.fixture(scope="function")
def app():
    return app_
