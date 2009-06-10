#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Little stupid program that rotate a stream of 90°, 180° or 270°'''

def rotate(istream, ostream, iencoding='utf8', oencoding='utf8'):
    """Dato uno stream di caratteri in input, lo consuma tutto, e scrive sullo
    stream di output ruotando il tutto di 90° in senso antiorario
    @warning: applicare 4 rotazioni *non* riporta lo stream allo stato iniziale,
            a causa degli spazi aggiuntivi necessari nelle rotazioni intermedie
    """
    matrix = [row.decode(iencoding)[:-1] for row in istream.readlines()]
    for i in range(max(len(row) for row in matrix)-1, -1, -1):
        buf = []
        for row in matrix:
            try:
                buf.append(row[i])
            except IndexError:
                buf.append(' ')
        ostream.write('%s\n' % ''.join(buf).encode(oencoding).rstrip())

def parse_options():
    """Create an OptionParser istance, add the user options and return the
    couple options, args"""
    from optparse import OptionParser
    parser = OptionParser(version='%prog 0.2',
            usage='%prog [OPTIONS] [INFILE [OUTFILE]]')
    parser.add_option('-r', '--rotate', default='90', action='store',
            metavar='N', choices=('90', '180', '270'),
            help='rotate N degree counter-clockwise (default=%default)')
    parser.add_option('-i', '--iencoding', default='utf8', action='store',
            metavar='E', help='set E as the input encoding (default=%default)')
    parser.add_option('-o', '--oencoding', default='utf8', action='store',
            metavar='E', help='set E as the output encoding (default=%default)')
    return parser.parse_args()

def check_args(args):
    """Parse args, and return a couple (istream, ostream)
    args should be a 0, 1 or 2 elements list, each of which should be a filename or '-'
    """
    from sys import stdin, stdout
    from os.path import isfile

    if not args:
        return stdin, stdout

    # check istream = (stdin|file)
    if args[0] == '-':
        istream = stdin
    elif not isfile(args[0]):
        raise SystemExit("'%s`: file not found" % args[0])
    else:
        istream = open(args[0])

    if len(args) == 1:
        return istream, stdout

    # check ostream = (stdout|file)
    if args[1] == '-':
        ostream = stdout
    elif isfile(args[1]):
        raise SystemExit("'%s`: file already found" % args[1])
    else:
        ostream = file(args[1], 'w')

    return istream, ostream

if __name__ == '__main__':
    OPTIONS, ARGS = parse_options()
    ISTREAM, OSTREAM = check_args(ARGS)
    rotate(ISTREAM, OSTREAM, OPTIONS.iencoding, OPTIONS.oencoding,
            OPTIONS.rotate)
