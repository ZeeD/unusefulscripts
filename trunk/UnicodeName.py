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

def main():
    '''Uso: UnicodeName [strings]*'''

    #fsenc = sys.getfilesystemencoding()
    sienc = sys.stdin.encoding  # better guess, I guess

    if len(sys.argv) < 2:
        raise SystemExit(u'Uso: %s [strings]*' % (sys.argv[0].decode(sienc), ))

    chars = (char for string in sys.argv[1:] for char in string.decode(sienc))

    for char, codepoint, category, name in data(chars):
        print(u'%s\t\\u%04x\t%s\t%s' % (char, codepoint, category, name))

if __name__ == '__main__':
    main()
