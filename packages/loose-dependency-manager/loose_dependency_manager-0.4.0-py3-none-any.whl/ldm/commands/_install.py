import os
from os import getcwd
from os.path import join, exists
from yaml_replace import YAMLTemplate
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

        self.logger.debug("Read configuration file: ")
        for line in config.model_dump_json(indent=2).split("\n"):
            self.logger.debug(line)

        Installer(logger=self.logger).install(config, targets)
        exit(0)


def read_config() -> DependencyConfig | None:
    if exists(CONFIG_FILE_NAME):
        with open(CONFIG_FILE_NAME, "r") as f:
            # Read configuration file
            template = YAMLTemplate(f.read())
            config = DependencyConfig(**template.render({}))

            # Load environment variables
            for env_file in config.config.environment.env_files:
                load_dotenv(dotenv_path=join(getcwd(), env_file))

            # Rerender configuration file with environment variables
            return DependencyConfig(**template.render(os.environ))
    return None
