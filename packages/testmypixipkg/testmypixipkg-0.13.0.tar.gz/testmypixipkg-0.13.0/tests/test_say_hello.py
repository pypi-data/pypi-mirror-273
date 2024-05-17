import pytest
from testmypixipkg import __main__


def test_say_hello():
    assert __main__.hello() == (
        "Hello, [bold magenta]World[/bold magenta]!",
        ":vampire:",
    )


if __name__ == "__main__":
    pytest.main()
