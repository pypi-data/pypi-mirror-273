from pydantic import BaseModel
from ..scheme import HTTPScheme
from ._factory import SchemeFactory


class HTTPSchemeFactoryConfig(BaseModel):
    encoding: str | None = None
    headers: dict | None = None
    cookies: dict | None = None


class HTTPSchemeFactory(SchemeFactory):
    name = "http"

    def create(
        self,
        config: dict | None = None,
    ) -> HTTPScheme:
        config: HTTPSchemeFactoryConfig = HTTPSchemeFactoryConfig(**(config or {}))
        return HTTPScheme(
            name=self.name,
            encoding=config.encoding,
            headers=config.headers,
            cookies=config.cookies,
            logger=self.logger,
        )
