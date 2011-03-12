#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unicodedata

def main():
    '''Uso: UnicodeName [strings]*'''

    fsenc = sys.getfilesystemencoding()

    if len(sys.argv) < 2:
        raise SystemExit(u'Uso: %s [strings]*' % (sys.argv[0].decode(fsenc), ))

    chars = (char for string in sys.argv[1:] for char in string.decode(fsenc))

    data = ((char, unicodedata.name(char)) for char in chars)

    for char, name in data:
        print u'%s\t%s' % (char, name)

if __name__ == '__main__':
    main()
