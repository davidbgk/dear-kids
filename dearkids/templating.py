import jinja2
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("dearkids", "templates"),
    autoescape=select_autoescape(["html"]),
)


def language_aware_template(template_name: str, language_code: str) -> jinja2.Template:
    try:
        return env.get_template(f"{language_code}.{template_name}")
    except jinja2.exceptions.TemplateNotFound:
        return env.get_template(template_name)
