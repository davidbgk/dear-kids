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


async def test_essay_submission(client, app):
    client.content_type = "application/x-www-form-urlencoded"
    resp = await client.post("/essay/", body={"essay": "foo"})
    assert resp.status == HTTPStatus.FOUND
    assert resp.headers["Location"].startswith("/essay/")
    resp = await client.get(resp.headers["Location"])
    assert resp.status == HTTPStatus.OK
    assert b"<p>foo</p>" in resp.body
