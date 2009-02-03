#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Programma scemo & idiota per convertire i file di testo di windows
# (usualmente codificati in cp1252) in utf8
# 2008-11-23 - Versione iniziale

if __name__ == '__main__':
    from sys import argv, stdin, stdout
    if len(argv) > 3 or set(('-h', '--help')).intersection(argv[1:]):
        raise SystemExit("USO: %s [INFILE [OUTFILE]]" % argv[0])
    try:
        infile = open(argv[1], "r")
    except IndexError:
        infile = stdin
    except IOError:
        raise SystemExit("Error: `%s' non esiste" % argv[1])
    try:
        outfile = open(argv[2], "w")
    except IndexError:
        outfile = stdout
    outfile.writelines(row.replace('\r', '').decode('cp1252').encode('utf8')
            for row in infile.readlines())
