from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_essay(client, app):
    resp = await client.get("/essay/sorry")
    assert resp.status == HTTPStatus.OK
    assert resp.headers["Content-Type"] == "text/html; charset=utf-8"
    assert b"<p><em>Deeply</em> sorry.</p>" in resp.body


async def test_essay_missing(client, app):
    resp = await client.get("/essay/notfound")
    assert resp.status == HTTPStatus.NOT_FOUND
    assert resp.body == b"Essay not found."
