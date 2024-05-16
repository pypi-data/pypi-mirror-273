from os import getcwd
from os.path import join
import click
from dotenv import load_dotenv
from ..commands import InstallCommand
from ._logger import create_logger
from ._error import error_boundary


@click.group()
def cli():
    load_dotenv(dotenv_path=join(getcwd(), ".env"))


@cli.command("install")
@click.argument("dependencies", nargs=-1)
def install(dependencies: list[str]):
    logger = create_logger()

    command = InstallCommand(logger=logger)
    error_boundary(
        lambda: command.run(targets=dependencies or None),
        logger,
    )
