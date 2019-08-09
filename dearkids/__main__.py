import asyncio
from http import HTTPStatus
from pathlib import Path

import uvloop
from commonmark import commonmark
from roll import HttpError
from roll import Roll as BaseRoll
from roll.extensions import logger, simple_server, static, traceback

from .extensions import i18n
from .request import CustomRequest
from .response import CustomResponse
from .templating import language_aware_template
from .utils import get_md_content_from_disk

HERE = Path(__file__)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Roll(BaseRoll):
    Request = CustomRequest
    Response = CustomResponse


app = Roll()
logger(app)
traceback(app)
static(app, root=HERE.parent / "static")
i18n(app)


@app.route("/")
async def home(request: CustomRequest, response: CustomResponse) -> None:
    template_name = "home.html"
    template = language_aware_template(template_name, request.language)
    response.html(template)


@app.route("/essay/{parameter}")
async def essay(
    request: CustomRequest, response: CustomResponse, parameter: str
) -> None:
    template_name = "essay.html"
    template = language_aware_template(template_name, request.language)
    try:
        md_content = get_md_content_from_disk(parameter)
    except FileNotFoundError:
        raise HttpError(HTTPStatus.NOT_FOUND, "Essay not found.")
    content = commonmark(md_content)
    response.html(template, content=content)


if __name__ == "__main__":
    simple_server(app)
