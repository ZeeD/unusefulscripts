#!/usr/bin/env python

from sys import argv
from unicodedata import category, name

if len(argv) < 2:
    raise SystemExit(f'Uso: {argv[0]} [strings]*')

for i, string in enumerate(argv[1:]):
    if i > 0:
        print()
    print(f'{string=!r}')
    for char in string:
        print(f'{char}\t\\U{ord(char):08x}\t{category(char)}\t{name(char)}')
