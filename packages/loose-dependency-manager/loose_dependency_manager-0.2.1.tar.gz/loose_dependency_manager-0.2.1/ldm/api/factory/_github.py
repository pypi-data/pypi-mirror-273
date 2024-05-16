from urllib.parse import urlparse, ParseResult
from pydantic import BaseModel
from ._factory import SchemeFactory
from ..scheme import GithubScheme


class GithubSchemeFactoryConfig(BaseModel):
    owner: str
    repo: str
    ref: str | None = None
    token: str | None = None

    @staticmethod
    def from_url(config: dict) -> "GithubSchemeFactoryConfig":
        url = config["url"]
        parsed: ParseResult = urlparse(url)
        path = parsed.path.lstrip("/")
        owner, repo = path.split("/")

        return GithubSchemeFactoryConfig(
            owner=owner,
            repo=repo,
            ref=config.get("ref"),
            token=config.get("token"),
        )


class GithubSchemeFactory(SchemeFactory):
    name = "github"

    def create(
        self,
        config: dict | None = None,
    ) -> GithubScheme:
        config: GithubSchemeFactoryConfig = config or {}
        if "url" in config:
            config = GithubSchemeFactoryConfig.from_url(config)
        else:
            config = GithubSchemeFactoryConfig(**config)
        return GithubScheme(
            name=self.name,
            owner=config.owner,
            repo=config.repo,
            ref=config.ref,
            token=config.token,
            logger=self.logger,
        )
