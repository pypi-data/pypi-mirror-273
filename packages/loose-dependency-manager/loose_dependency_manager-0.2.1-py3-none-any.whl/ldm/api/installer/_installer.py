from typing import Generator
from urllib.parse import urlparse
from ldm.logger import Logger
from ..config import DependencyConfig, SchemeConfig
from ..scheme import Scheme
from ..factory import HTTPSchemeFactory, HTTPSSchemeFactory, GithubSchemeFactory
from ...component import Component
from ..parse import parse_entry
from ._dependency import Dependency
from .strategy import create_install_strategy


class Installer(Component):
    def __init__(
        self,
        *,
        logger: Logger | None = None,
    ) -> None:
        super().__init__(logger)
        self.schemes: dict[str, Scheme] = {
            # Default schemes
            "http": HTTPSchemeFactory(logger=self.logger).create({}),
            "https": HTTPSSchemeFactory(logger=self.logger).create({}),
        }

    def install(
        self,
        config: dict,
        targets: list[str] | None = None,
    ) -> None:
        def parse_schemes(schemes: dict[str, SchemeConfig]) -> dict[str, Scheme]:
            def create_scheme(
                name: str,
                scheme_config: SchemeConfig,
            ) -> tuple[str, Scheme]:
                factory = {
                    "github": GithubSchemeFactory,
                    "http": HTTPSchemeFactory,
                    "https": HTTPSSchemeFactory,
                }[scheme_config.uses]
                return name, factory(logger=self.logger).create(scheme_config.with_)

            def create_schemes(
                schemes: dict[str, SchemeConfig],
            ) -> Generator[tuple[str, Scheme], None, None]:
                for name, scheme_config in schemes.items():
                    yield create_scheme(name, scheme_config)

            return dict(list(create_schemes(schemes)))

        def parse_dependencies(
            dependencies: dict[str, str],
        ) -> Generator[Dependency, None, None]:
            def decide_scheme(entry: str) -> str:
                source, _ = parse_entry(entry)
                parsed = urlparse(source)
                return parsed.scheme

            def parse_dependency(
                name: str,
                entry: str,
            ) -> Dependency:
                scheme = decide_scheme(entry)
                return Dependency(
                    name,
                    lambda: self.schemes[scheme].install(entry),
                )

            for name, entry in dependencies.items():
                yield parse_dependency(name, entry)

        self.logger.info("Installing dependencies...")

        config: DependencyConfig = DependencyConfig(**config)

        self.schemes.update(parse_schemes(config.schemes))

        strategy = create_install_strategy(
            config.config.strategy,
            config.config,
            logger=self.logger,
        )

        dependencies = list(parse_dependencies(config.dependencies))
        if targets is not None:
            dependencies = list(filter(lambda d: d.name in targets, dependencies))

        strategy.install(dependencies)

        self.logger.success("Dependencies installed")
