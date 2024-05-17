from rich import print


def hello():
    return "Hello, [bold magenta]World[/bold magenta]!", ":vampire:"


def say_hello():
    print(*hello())


if "__main__" == __name__:
    say_hello()
