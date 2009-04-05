#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sys import stdin, stdout

def rotate(istream=stdin, ostream=stdout, iencoding='utf8', oencoding='utf8'):
    """Dato uno stream di caratteri in input, lo consuma tutto, e scrive sullo
    stream di output ruotando il tutto di 90° in senso antiorario
    @warning: applicare 4 rotazioni *non* riporta lo stream allo stato iniziale,
            a causa degli spazi aggiuntivi necessari nelle rotazioni intermedie
    """
    matrix = [row.decode(iencoding)[:-1] for row in istream.readlines()]
    for i in range(max(len(row) for row in matrix)-1, -1, -1):
        buffer = []
        for row in matrix:
            try:
                buffer.append(row[i])
            except IndexError:
                buffer.append(' ')
        ostream.write('%s\n' % ''.join(buffer).encode(oencoding).rstrip())

if __name__ == '__main__':
    from sys import argv
    from os.path import isfile
    if len(argv) > 1:
        if argv[1] == '-':
            istream = stdin
        elif not isfile(argv[1]):
            raise SystemExit("'%s`: file not found" % argv[1])
        else:
            istream = open(argv[1])
        if len(argv) > 2:
            if argv[2] == '-':
                ostream = stdout
            elif isfile(argv[2]):
                raise SystemExit("'%s`: file already found" % argv[2])
            else:
                ostream = file(argv[2], 'w')
            rotate(istream, ostream)
        else:
            rotate(istream)
    else:
        rotate()
