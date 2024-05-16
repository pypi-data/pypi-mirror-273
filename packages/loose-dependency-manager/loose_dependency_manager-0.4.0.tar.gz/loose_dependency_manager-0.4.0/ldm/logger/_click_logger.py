import sys
import click
from ._logger import Logger


class ClickLogger(Logger):
    def debug(self, message: str, *args, **kwargs) -> None:
        if self.level > 1:
            return
        kwargs.setdefault("fg", "blue")
        message = f"[ldm] |   DEBUG | {message}"
        click.echo(
            click.style(message, *args, **kwargs),
            file=sys.stdout,
        )

    def info(self, message: str, *args, **kwargs) -> None:
        if self.level > 2:
            return
        message = f"[ldm] |    INFO | {message}"
        click.echo(
            click.style(message, *args, **kwargs),
            file=sys.stdout,
        )

    def success(self, message: str, *args, **kwargs) -> None:
        if self.level > 3:
            return
        message = f"[ldm] | SUCCESS | {message}"
        kwargs.setdefault("fg", "green")
        click.echo(
            click.style(message, *args, **kwargs),
            file=sys.stdout,
        )

    def warning(self, message: str, *args, **kwargs) -> None:
        if self.level > 4:
            return
        message = f"[ldm] | WARNING | {message}"
        kwargs.setdefault("fg", "yellow")
        click.echo(
            click.style(message, *args, **kwargs),
            file=sys.stdout,
        )

    def error(self, message: str, *args, **kwargs) -> None:
        if self.level > 5:
            return
        message = f"[ldm] |   ERROR | {message}"
        kwargs.setdefault("fg", "red")
        click.echo(
            click.style(message, *args, **kwargs),
            file=sys.stderr,
        )
