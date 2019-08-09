from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


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
