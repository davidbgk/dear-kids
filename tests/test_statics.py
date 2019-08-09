from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_stylesheet(client, app):
    resp = await client.get("/static/styles.css")
    assert resp.status == HTTPStatus.OK
    assert resp.headers["Content-Type"] == "text/css"
    assert resp.body.startswith(b":root {")
