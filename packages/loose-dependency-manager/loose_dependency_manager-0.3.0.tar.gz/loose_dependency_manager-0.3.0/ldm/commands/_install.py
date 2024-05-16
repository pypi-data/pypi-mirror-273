import os
from os import getcwd
from os.path import join
from yaml_replace import YAMLTemplate
from os.path import exists
from ._command import Command
from ..api.installer import Installer
from ..api.config import CONFIG_FILE_NAME, DependencyConfig
from dotenv import load_dotenv


class InstallCommand(Command):
    def run(self, targets: list[str] | None = None):
        # Read configuration file
        config = read_config()
        if config is None:
            self.logger.error("No configuration file found")
            exit(1)

        # Load environment variables
        for env_file in config.config.environment.env_files:
            load_dotenv(dotenv_path=join(getcwd(), env_file))

        Installer(logger=self.logger).install(config, targets)
        exit(0)


def read_config() -> DependencyConfig | None:
    if exists(CONFIG_FILE_NAME):
        with open(CONFIG_FILE_NAME, "r") as f:
            config = YAMLTemplate(f.read()).render(dict(os.environ))
            return DependencyConfig(**config)
    return None
