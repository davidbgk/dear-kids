import asyncio
from pathlib import Path

import uvloop
from jinja2 import Environment, PackageLoader, select_autoescape
from roll import Response
from roll import Roll as BaseRoll
from roll.extensions import logger, simple_server, static, traceback

HERE = Path(__file__)

env = Environment(
    loader=PackageLoader("dearkids", "templates"),
    autoescape=select_autoescape(["html"]),
)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class HTMLResponse(Response):
    def html(self, template_name, *args, **kwargs):
        self.headers["Content-Type"] = "text/html; charset=utf-8"
        self.body = env.get_template(template_name).render(*args, **kwargs)


class Roll(BaseRoll):
    Response = HTMLResponse


app = Roll()
logger(app)
traceback(app)
static(app, root=HERE.parent / "static")


@app.route("/")
async def home(request, response):
    response.html("home.html")


if __name__ == "__main__":
    simple_server(app)
