from accept_language import parse_accept_language
from roll import Request, Response


def i18n(app):
    @app.listen("request")
    async def guess_language(request: Request, response: Response):
        language = "en"
        accept_language_header = request.headers.get("ACCEPT-LANGUAGE")
        languages = parse_accept_language(accept_language_header)
        if languages:
            language = languages[0].language
        request["language"] = language
