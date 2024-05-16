from ...config import SequentialConfig
from ._strategy import InstallStrategy


class SequentialInstallStrategy(InstallStrategy[SequentialConfig]):
    def install(self, dependencies):
        self.logger.debug("Installing dependencies sequentially")
        for dependency in dependencies:
            dependency.install()
            self.logger.info(f"Installed {dependency.name}")
