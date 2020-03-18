"""Runs the console application by default."""

import sys  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    from .console import main

    sys.exit(main())
