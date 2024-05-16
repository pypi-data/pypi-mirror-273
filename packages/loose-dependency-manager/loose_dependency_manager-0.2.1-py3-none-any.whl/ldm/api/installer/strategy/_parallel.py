from concurrent.futures import ThreadPoolExecutor
from ...config import ParallelConfig
from .._dependency import Dependency
from ._strategy import InstallStrategy


class ParallelInstallStrategy(InstallStrategy[ParallelConfig]):
    def install(self, dependencies):
        self.logger.debug("Installing dependencies in parallel")
        with ThreadPoolExecutor(max_workers=self.config.workers) as executor:

            def create_install_task(dependency: Dependency) -> None:
                def install():
                    dependency.install()
                    self.logger.info(f"Installed {dependency.name}")

                return install

            futures = [
                executor.submit(create_install_task(dependency))
                for dependency in dependencies
            ]

            for future in futures:
                future.result()
