from http import HTTPStatus

import pytest

from dearkids import app as app_

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
def app():
    return app_


async def test_home(client, app):
    resp = await client.get("/")
    assert resp.status == HTTPStatus.OK
    assert b"<h1>Dear kids,</h1>" in resp.body
