import httpx
from os import makedirs
from os.path import exists, dirname
from ldm.logger import Logger
from ..parse import parse_entry
from ._scheme import Scheme


class HTTPScheme(Scheme):
    def __init__(
        self,
        name: str,
        encoding: str | None = None,
        headers: dict | None = None,
        cookies: dict | None = None,
        *,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(name, logger=logger)
        self.encoding = encoding or "utf-8"
        self.headers = headers
        self.cookies = cookies

    def install(self, entry: str) -> None:
        # Parse the entry
        source, destination = parse_entry(entry)

        content = httpx.get(
            source,
            headers=self.headers,
            cookies=self.cookies,
        ).content.decode(self.encoding)

        if not exists(dirname(destination)):
            makedirs(dirname(destination), exist_ok=True)

        with open(destination, "w") as f:
            f.write(content)
