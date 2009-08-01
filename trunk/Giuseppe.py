#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: farla ricorsiva e usando itertools.cycle

def Giuseppe(total, skip):
    '''Banale soluzione per il problema di Giuseppe <_http://it.wikipedia.org/wiki/Problema_di_Giuseppe
    '''
    total = range(1, total+1)
    skip -= 1
    current = 0
    while (len(total) > 1):
        current = (current+skip) % len(total)
        del total[current]
    return total[0]

if __name__ == '__main__':
    from sys import argv
    total, skip = map(int, argv[1:3])
    print(josefus(total, skip))
