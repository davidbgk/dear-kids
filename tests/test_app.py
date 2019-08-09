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
    assert resp.headers["Content-Type"] == "text/html; charset=utf-8"
    assert b"<h1>Dear kids,</h1>" in resp.body


async def test_home_fr(client, app):
    resp = await client.get("/", headers={"Accept-language": "fr-CA"})
    assert resp.status == HTTPStatus.OK
    assert resp.headers["Content-Type"] == "text/html; charset=utf-8"
    assert b"<h1>Les enfants,</h1>" in resp.body


async def test_stylesheet(client, app):
    resp = await client.get("/static/styles.css")
    assert resp.status == HTTPStatus.OK
    assert resp.headers["Content-Type"] == "text/css"
    assert resp.body.startswith(b":root {")
