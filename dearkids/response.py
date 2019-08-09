import jinja2
from roll import Response


class CustomResponse(Response):
    def html(self, template: jinja2.Template, *args, **kwargs) -> None:
        self.headers["Content-Type"] = "text/html; charset=utf-8"
        self.body = template.render(*args, **kwargs)
