#!/usr/bin/env python
# -*- coding: utf-8 -*-

def raggruppamenti(pagine_totali, base):
    """FIXME: Shlemiel the painter's algorithm! (my pc is fast enougth -.-)"""
    pagine_per_raggruppamento = 0
    while pagine_per_raggruppamento < pagine_totali:
        numero_raggruppamenti = 0
        pagine_per_raggruppamento += base
        while numero_raggruppamenti * pagine_per_raggruppamento < pagine_totali:
            numero_raggruppamenti += 1
        yield pagine_per_raggruppamento, numero_raggruppamenti

def usage(program_name):
    from sys import stderr
    stderr.write("Uso: %s PAGINE_TOTALI [BASE=4]\n" % program_name)

def print_one_row(headers_l, format, pt, ppr, nr):
    ps = ppr * nr
    elements = (ppr, nr, ps, pt, ps-pt)
    print format % tuple(str(n).center(l) for n,l in zip(elements, headers_l))

def print_output(headers, format, pagine_totali, base, show_all=False):
    from itertools import groupby
    print format_string % headers
    print "-" * (sum(map(len, headers)) + 14) # " * ", " == ", " == ", " + "
    headers_l = map(len, headers)
    if show_all:
        for pagine_per_raggruppamento, numero_raggruppamenti in raggruppamenti(
                pagine_totali, base):
            print_one_row(headers_l, format, pagine_totali,
                    pagine_per_raggruppamento, numero_raggruppamenti)
    else:
        for pagine_per_raggruppamento, numero_raggruppamenti in (min(el[1])
                for el in groupby(raggruppamenti(pagine_totali, base),
                        lambda e: e[1])):
            print_one_row(headers_l, format, pagine_totali,
                    pagine_per_raggruppamento, numero_raggruppamenti)

if __name__ == '__main__':
    from sys import argv
    try:
        pagine_totali = int(argv[1])
    except:
        raise SystemExit(usage(argv[0]))
    try:
        base = int(argv[2])
    except:
        base = 4
    headers = ("pagine_per_raggruppamento", "numero_raggruppamenti",
            "pagine_stampate", "pagine_totali", "bianche")
    format_string = "%s * %s == %s == %s + %s"
    print_output(headers, format_string, pagine_totali, base, True)
    print_output(headers, format_string, pagine_totali, base, False)
