from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from sys import argv
from typing import NoReturn

logger = getLogger(__name__)


def prepend(text: str, filename: Path) -> None:
    raise NotImplementedError


def usage(name: str = argv[0]) -> NoReturn:
    logger.error('usage: %s text filename', name)
    raise SystemExit


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    try:
        _, text, fn = argv
    except ValueError:
        usage()

    if '-h' in {text, fn} or '--help' in {text, fn}:
        usage()

    prepend(text, Path(fn))


if __name__ == '__main__':
    main()
