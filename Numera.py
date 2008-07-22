#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2007-08-04 - versione in utf-8
# 2007-03-11 - Uso di optparse per capire che cavolo fa il programma
# 2006-04-23
# numera.py

from optparse import OptionParser
from os import rename
from os.path import isfile, exists
from warnings import warn

parser = OptionParser(
    version = '%prog 0.2.0',
    usage = '''%prog [FILE|"" [FILES_OR_NOTHING]]
    Mette un numero in ordine crescente davanti ad ogni FILE specificato'''
)
parser.add_option('-b', '--begin', type="int", default=1, metavar='N', help="start to numerate from N")
parser.add_option('-v', '--verbose', action='store_true', default=False, help="show on STDOUT what happens")
parser.add_option('-c', '--cifre', type="int", default=0, metavar='N', help="use at least N chars to represents the numbers")

options, args = parser.parse_args()

associa=[]
for parametro in args:
    if isfile(parametro):
        associa.append((parametro, options.begin))
    elif parametro is '':
        pass
    else:
        warn(parametro+" non è ne' un file ne' ''", SyntaxWarning, 2)
    options.begin += 1

formato = '%%.%dd - ' % max(options.cifre, len(str(associa[-1][1])))

for sorgente, intero in associa:
    destinazione = formato % intero + sorgente
    if not exists(destinazione):
        if options.verbose:
            print sorgente, '->', destinazione
        rename(sorgente, destinazione)
    else:
        warn(destinazione+' è già usato!', RuntimeWarning, 2)
