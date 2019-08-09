import asyncio
from pathlib import Path

import jinja2
import uvloop
from jinja2 import Environment, PackageLoader, select_autoescape
from roll import Request, Response
from roll import Roll as BaseRoll
from roll.extensions import logger, simple_server, static, traceback

HERE = Path(__file__)

env = Environment(
    loader=PackageLoader("dearkids", "templates"),
    autoescape=select_autoescape(["html"]),
)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def i18n(app):
    @app.listen("request")
    async def guess_language(request, response):
        accept_language = request.headers.get("ACCEPT-LANGUAGE")
        # Very naive, yet very efficient?
        request.language = accept_language[:2] if accept_language else "en"


class LanguageAwareRequest(Request):
    __slots__ = (
        "app",
        "url",
        "path",
        "query_string",
        "_query",
        "method",
        "body",
        "headers",
        "route",
        "_cookies",
        "_form",
        "_files",
        "language",  # Added.
    )


class HTMLResponse(Response):
    def html(self, template, *args, **kwargs):
        self.headers["Content-Type"] = "text/html; charset=utf-8"
        self.body = template.render(*args, **kwargs)


class Roll(BaseRoll):
    Request = LanguageAwareRequest
    Response = HTMLResponse


app = Roll()
logger(app)
traceback(app)
static(app, root=HERE.parent / "static")
i18n(app)


def language_aware_template(template_name, language_code):
    try:
        return env.get_template(f"{language_code}.{template_name}")
    except jinja2.exceptions.TemplateNotFound:
        return env.get_template(template_name)


@app.route("/")
async def home(request, response):
    template_name = "home.html"
    template = language_aware_template(template_name, request.language)
    response.html(template)


if __name__ == "__main__":
    simple_server(app)
