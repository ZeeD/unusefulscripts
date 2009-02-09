#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby

def trovaRaggruppamenti(pagine_totali, base=4):
    trovati = []
    i = 1
    while (base*i) < pagine_totali:
        numero_gruppi = base*i
        pagine_per_gruppo = pagine_totali/numero_gruppi + (1
                if pagine_totali%numero_gruppi else 0)
        trovati.append((numero_gruppi, pagine_per_gruppo,
                numero_gruppi*pagine_per_gruppo - pagine_totali))
        i += 1
    return groupby(trovati, lambda x:x[1])

def usage(argv):
    from sys import stderr
    stderr.write("Uso: %s NUM_PAGINE\n" % argv[0])
    raise SystemExit

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 1:
        usage(argv)
    for element in argv[1:]:
        try:
            pagine = int(element)
        except:
            usage(argv)
        else:
            if len(argv) != 2:
                print "pagine: ", pagine
            print "Numero gruppi\tPagine per gruppo (facciate bianche)"
            for key, it in trovaRaggruppamenti(pagine):
                r = ', '.join("%d(%d)" % (el[0], el[2]) for el in it)
                print "\t%d\t%s" % (key, r)
