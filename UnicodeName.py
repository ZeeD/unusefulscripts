#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unicodedata

def data(chars):
    for char in chars:
        codepoint = ord(char)
        category = unicodedata.category(char)
        try:
            name = unicodedata.name(char)
        except Exception as e:
            print('\t\t%s -> %s' % (char, e))
            continue
        yield (char, codepoint, category, name)

def c(sys, sienc):
    for string in sys.argv[1:]:
        print(u'c  -> string: %r' % (string, ))
        ustring = string.decode(sienc)
        print(u'c  -> ustring: %r' % (ustring, ))
        for char in ustring:
            print(u'c  -> char: %s' % (char, ))
            yield char

def main():
    '''Uso: UnicodeName [strings]*'''

    #fsenc = sys.getfilesystemencoding()
    sienc = sys.stdin.encoding  # better guess, I guess

    if len(sys.argv) < 2:
        raise SystemExit(u'Uso: %s [strings]*' % (sys.argv[0].decode(sienc), ))

    from pprint import pprint
    pprint(sys.argv[1:][0].decode('UTF-8'))

    chars = c(sys, sienc)

    chars = list(chars)
    pprint(chars)

    for char, codepoint, category, name in data(chars):
        print(u'%s\t\\u%04x\t%s\t%s' % (char, codepoint, category, name))

if __name__ == '__main__':
    main()
