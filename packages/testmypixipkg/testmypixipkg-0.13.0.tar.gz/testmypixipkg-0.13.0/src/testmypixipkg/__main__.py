"""This module contains the main functionality of the testmypixipkg package."""

from rich import print


def hello() -> tuple[str, str]:
    """Return a greeting message and an emoji."""
    return "Hello, [bold magenta]World[/bold magenta]!", ":vampire:"


def say_hello() -> None:
    """Print a greeting message and an emoji."""
    print(*hello())


if "__main__" == __name__:
    say_hello()
