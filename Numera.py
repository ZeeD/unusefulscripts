#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2007-08-04 - versione in utf-8
# 2007-03-11 - Uso di optparse per capire che cavolo fa il programma
# 2006-04-23
# numera.py

from optparse import OptionParser
from os import rename
from os.path import exists
from math import log

def number_len(i, base=10):
    """Calcola il numero di cifre necessarie per un numero in una certa base"""
    i = int(i) # se non è un intero, o trasformabile in esso, piangi
    if i == 0:
        return 1
    return int(log(i, base)) + (1 if i > 0 else 2) # 2 è per il segno -

if __name__ == '__main__':
    parser = OptionParser(version='%prog 0.2.0', usage='''%prog (FILE|"")...
        Mette un numero in ordine crescente davanti ad ogni FILE specificato
        Usa "" per inserire "buchi"''')
    parser.add_option('-b', '--begin', type='int', default=1, metavar='N',
            help='Inizia a numerare da N (default = %default)')
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help='Mostra sullo STDOUT cosa accade')
    parser.add_option('-c', '--cifre', type='int', default=0, metavar='N',
            help='Usa almeno N cifre per i numeri (default = %default)')
    parser.add_option('-t', '--test', action='store_true', default=False,
            help='Non effettuare davvero la rinomina dei file (utile con -v)')

    options, args = parser.parse_args()

    max_number = 0
    substitutions = []
    for pos, param in enumerate(args):
        max_number = options.begin + pos
        if param:
            substitutions.append((param, max_number))

    format = '%%.%dd - ' % max(options.cifre, number_len(max_number))

    for source, number in substitutions:
        dest = format % number + source
        if not exists(dest):
            if options.verbose:
                print source, '->', dest
            if not options.test:
                rename(source, dest)
        else:
            warn(dest + ' è già usato!', RuntimeWarning, 2)

