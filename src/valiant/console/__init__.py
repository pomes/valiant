"""CLI configuration package."""
from .cli import Cli  # pragma: no cover


def main() -> int:  # pragma: no cover
    """Runs the CLI.

    Returns:
        A status code.
    """
    return Cli().run()
