from ._scheme import Scheme
from ldm.logger import Logger
from urllib.parse import urlparse
from gget import get_remote_file


class GithubScheme(Scheme):
    def __init__(
        self,
        name: str,
        owner: str,
        repo: str,
        ref: str = "HEAD",
        token: str | None = None,
        *,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(name, logger=logger)
        self.owner = owner
        self.repo = repo
        self.ref = ref
        self.token = token

    def install(self, entry: str) -> None:
        # Parse the entry
        source, destination = (
            entry.replace(" ", "").replace("\t", "").replace("\n", "").split("->")
        )
        parsed = urlparse(source)

        path = parsed.path

        get_remote_file(
            path=path,
            reponame=self.repo,
            owner=self.owner,
            output=destination,
            ref=self.ref,
            provider="github",
            provider_options={"token": self.token},
        )
