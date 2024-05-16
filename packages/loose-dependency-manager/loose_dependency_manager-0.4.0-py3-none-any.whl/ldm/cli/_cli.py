import click
from ..commands import InstallCommand
from ._logger import create_logger
from ._error import error_boundary


@click.group()
def cli():
    pass


@cli.command("install")
@click.argument("dependencies", nargs=-1)
@click.option("--debug", is_flag=True, default=False)
def install(dependencies: list[str], debug: bool):
    logger = create_logger(debug)

    command = InstallCommand(logger=logger)
    error_boundary(
        lambda: command.run(targets=dependencies or None),
        logger,
    )
