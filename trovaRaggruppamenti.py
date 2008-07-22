#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2007-12-31
# trovaRaggruppamenti.py

from itertools import groupby
def trovaRaggruppamenti(numeroPagineTotali, base = 4):
    trovati = []
    i = 1
    while (base*i) < numeroPagineTotali:
        raggruppamenti = base*i
        trovati.append((raggruppamenti,
                numeroPagineTotali/raggruppamenti +
                (1 if numeroPagineTotali%raggruppamenti else 0)))
        i += 1
    return groupby(trovati, lambda x:x[1])

if __name__ == '__main__':
    from sys import argv
    argv = argv[1:]
    for element in argv:
        try:
            pagine = int(element)
        except:
            pass
        else:
            if len(argv) != 1:
                print "pagine: ", pagine
            print "Numero gruppi\tPagine per gruppo"
            for key, it in trovaRaggruppamenti(pagine):
                print "\t%s\t" % key,
                for el in it:
                    print el[0],
                print
