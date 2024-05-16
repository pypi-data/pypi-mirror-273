import os
from yaml_replace import YAMLTemplate
from os.path import exists
from ._command import Command
from ..api.installer import Installer
from ..api.config import CONFIG_FILE_NAME


class InstallCommand(Command):
    def run(self, targets: list[str] | None = None):
        def read_config() -> dict | None:
            if exists(CONFIG_FILE_NAME):
                with open(CONFIG_FILE_NAME, "r") as f:
                    return YAMLTemplate(f.read()).render(dict(os.environ))
            return None

        config = read_config()

        if config is None:
            self.logger.error("No configuration file found")
            exit(1)

        Installer(logger=self.logger).install(config, targets)
        exit(0)
