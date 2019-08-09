import asyncio
from pathlib import Path

import jinja2
import uvloop
from accept_language import parse_accept_language
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
    async def guess_language(request: LanguageAwareRequest, response: Response):
        language = "en"
        accept_language_header = request.headers.get("ACCEPT-LANGUAGE")
        languages = parse_accept_language(accept_language_header)
        if languages:
            language = languages[0].language
        request.language = language


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
    def html(self, template: jinja2.Template, *args, **kwargs) -> None:
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


def language_aware_template(template_name: str, language_code: str) -> jinja2.Template:
    try:
        return env.get_template(f"{language_code}.{template_name}")
    except jinja2.exceptions.TemplateNotFound:
        return env.get_template(template_name)


@app.route("/")
async def home(request: LanguageAwareRequest, response: HTMLResponse) -> None:
    template_name = "home.html"
    template = language_aware_template(template_name, request.language)
    response.html(template)


if __name__ == "__main__":
    simple_server(app)
