#!/usr/bin/env python
# -*- coding: utf-8 -*-

def raggruppamenti(pagine_totali):
    """FIXME: Shlemiel the painter's algorithm! (my pc is fast enougth -.-)"""
    pagine_per_raggruppamento = 0
    while pagine_per_raggruppamento < pagine_totali:
        numero_raggruppamenti = 0
        pagine_per_raggruppamento += 4
        while numero_raggruppamenti * pagine_per_raggruppamento < pagine_totali:
            numero_raggruppamenti += 1
        yield pagine_per_raggruppamento, numero_raggruppamenti

def print_one_row(headers_l, format, pt, ppr, nr):
    ps = ppr * nr
    elements = (ppr, nr, ps, pt, ps-pt)
    print format % tuple(str(n).center(l) for n,l in zip(elements, headers_l))

def print_output(headers, format, pagine_totali, show_all=False):
    from itertools import groupby
    print format_string % headers
    print "-" * (sum(map(len, headers)) + 14) # " * ", " == ", " == ", " + "
    headers_l = map(len, headers)
    if show_all:
        for pagine_per_raggruppamento, numero_raggruppamenti in raggruppamenti(
                pagine_totali):
            print_one_row(headers_l, format, pagine_totali,
                    pagine_per_raggruppamento, numero_raggruppamenti)
    else:
        for pagine_per_raggruppamento, numero_raggruppamenti in (min(el[1])
                for el in groupby(raggruppamenti(pagine_totali),
                        lambda e: e[1])):
            print_one_row(headers_l, format, pagine_totali,
                    pagine_per_raggruppamento, numero_raggruppamenti)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(version='%prog 0.3.0', usage='''%prog PAGINE_TOTALI...
        Genera le possibili combinazioni per stampare PAGINE_TOTALI pagine''')
    parser.add_option('-a', '--all', action='store_true', default=False,
            help='Mostra tutte le possibili combinazioni')
    options, args = parser.parse_args()

    headers = ("pagine_per_raggruppamento", "numero_raggruppamenti",
            "pagine_stampate", "pagine_totali", "bianche")
    format_string = "%s * %s == %s == %s + %s"

    if not args:
        raise SystemExit(parser.print_usage())

    for arg in args:
        try:
            pagine_totali = int(arg)
        except:
            raise RuntimeWarning("`%s' non è un numero!" % arg)
        print_output(headers, format_string, pagine_totali, options.all)
