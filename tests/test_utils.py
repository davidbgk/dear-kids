import pytest

from dearkids.__main__ import ALLOWED_TAGS
from dearkids.utils import escape_content

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "input,output",
    [
        ("foo", "foo"),
        (
            "<p><em><strong>bar</strong></em></p>",
            "<p><em><strong>bar</strong></em></p>",
        ),
        ("<em><a href='/'>baz</a></em>", "<em>baz</em>"),
        ("http://dear-kids.example.com", "http://dear-kids.example.com"),
    ],
)
async def test_escape_content(input, output):
    assert escape_content(input, allowed_tags=ALLOWED_TAGS) == output
