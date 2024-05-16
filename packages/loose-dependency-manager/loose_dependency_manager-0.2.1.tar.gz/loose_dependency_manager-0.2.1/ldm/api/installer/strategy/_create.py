from typing import Literal, Any
from ldm.logger import Logger
from ._strategy import InstallStrategy
from ._sequential import SequentialInstallStrategy
from ._parallel import ParallelInstallStrategy


def create_install_strategy(
    strategy: Literal["sequential", "parallel"],
    config: Any,
    logger: Logger | None = None,
) -> InstallStrategy:
    if strategy == "sequential":
        return SequentialInstallStrategy(config.sequential, logger=logger)
    elif strategy == "parallel":
        return ParallelInstallStrategy(config.parallel, logger=logger)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
