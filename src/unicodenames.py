from logging import INFO
from logging import basicConfig
from logging import error
from logging import getLogger
from sys import argv
from unicodedata import category
from unicodedata import name

logger = getLogger(__name__)


def unicode_names(string: str) -> list[str]:
    return [
        f'{char}\t\\U{ord(char):08x}\t{category(char)}\t{name(char)}'
        for char in string
    ]


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')

    argv0, *args = argv

    if not args:
        error('Uso: %s [strings]*', argv0)
        raise SystemExit(-1)

    for i, string in enumerate(args):
        if i > 0:
            logger.info('')
        logger.info('string: %r', string)
        for name_ in unicode_names(string):
            logger.info(name_)


if __name__ == '__main__':
    main()
