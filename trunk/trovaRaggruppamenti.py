#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby

def trovaRaggruppamenti(pagine_totali, base=4):
    trovati = []
    i = 1
    while (base*i) < pagine_totali:
        raggruppamenti = base*i
        resto = pagine_totali%raggruppamenti
        trovati.append((raggruppamenti,
                pagine_totali/raggruppamenti + (1 if resto else 0),
                resto))
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
