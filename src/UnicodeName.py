#!/usr/bin/env python

from logging import INFO
from logging import basicConfig
from logging import error
from logging import info
from sys import argv
from unicodedata import category
from unicodedata import name


def unicode_name(string: str) -> list[str]:
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
            info('')
        info('string: %r', string)
        for name_ in unicode_name(string):
            info(name_)


if __name__ == '__main__':
    main()

