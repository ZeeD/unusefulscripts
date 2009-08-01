#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Date n persone in circolo, si saltano k−1 persone e si giustizia la k-esima;
si ripete finché non rimane una sola persona, che viene graziata.
Determinare la posizione del sopravvissuto all'interno del cerchio iniziale.
'''

def soluzione_itertools(total, skip):
    '''Uso di itertools.cycle'''
    from itertools import cycle
    cycle(range(1, total+1))
    # TODO farla
    return 0

def soluzione_ricorsiva(total, skip):
    '''Uso di una funzione interna, ricorsiva'''
    def sol(total):
        '''funzione ricorsiva di supporto'''
        if len(total) == 1:
            return total[0]
        return sol(total[:skip-1] + total[skip+1:])
    return sol(range(1, total+1))

def soluzione_banale(total, skip):
    '''Banale soluzione per il problema di Giuseppe
    <_http://it.wikipedia.org/wiki/Problema_di_Giuseppe>'''
    total = range(1, total+1)
    skip -= 1
    current = 0
    while (len(total) > 1):
        current = (current+skip) % len(total)
        del total[current]
    return total[0]

if __name__ == '__main__':
    from sys import argv
    print(soluzione_banale(int(argv[1]), int(argv[2])))
