import asyncio
from http import HTTPStatus
from pathlib import Path

import uvloop
from commonmark import commonmark
from roll import HttpError, Request
from roll import Roll as BaseRoll
from roll.extensions import logger, simple_server, static, traceback

from .extensions import i18n
from .response import CustomResponse
from .templating import language_aware_template
from .utils import get_md_content_from_disk, save_md_content_to_disk

HERE = Path(__file__)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class Roll(BaseRoll):
    Response = CustomResponse


app = Roll()
logger(app)
traceback(app)
static(app, root=HERE.parent / "static")
i18n(app)


@app.route("/")
async def home(request: Request, response: CustomResponse) -> None:
    template_name = "home.html"
    template = language_aware_template(template_name, request["language"])
    response.html(template)


@app.route("/essay/", methods=["POST"])
async def on_post(request: Request, response: CustomResponse) -> None:
    essay_content = request.form.get("essay")
    name = save_md_content_to_disk(essay_content)
    response.status = HTTPStatus.FOUND
    response.headers["Location"] = f"/essay/{name}"


@app.route("/essay/{parameter}")
async def essay(request: Request, response: CustomResponse, parameter: str) -> None:
    template_name = "essay.html"
    template = language_aware_template(template_name, request["language"])
    try:
        md_content = get_md_content_from_disk(parameter)
    except FileNotFoundError:
        raise HttpError(HTTPStatus.NOT_FOUND, "Essay not found.")
    content = commonmark(md_content)
    response.html(template, content=content)


def run() -> None:
    simple_server(app)
