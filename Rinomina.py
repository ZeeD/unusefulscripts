#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2007-08-04 - versione in utf-8
# 2007-05-15 - Aggiunta di una opzione per usare il nome della directory come nome del file
# 2007-03-11 - Uso di optparse per capire che cavolo fa il programma
# 2006-04-23
# enumera.py

from optparse import OptionParser, OptionValueError
from os import chdir, listdir, rename
from os.path import abspath, basename, curdir, exists, splitext
from warnings import warn

def check_dir(option, opt, value, parser):
    from os.path import isdir
    if isdir(value):
        parser.values.dir = value
    else:
        raise OptionValueError(value + " isn't a directory")

parser = OptionParser(
    version = '%prog 0.2.5',
    usage = '''%prog [options] [NUMERI_SCARTATI|...]
    Mette un numero in ordine crescente davanti ad ogni file
    della directory specificata ignorando i NUMERI_SCARTATI'''
)
parser.add_option('-d', '--dir', action="callback", callback=check_dir, type='string', default='.', help="enumerate files located in DIR (default='.')")
parser.add_option('-b', '--begin', type="int", default=1, metavar='N', help="start to enumerate from N (default=1)")
parser.add_option('-v', '--verbose', action='store_true', default=False, help="show on STDOUT what happens")
parser.add_option('-c', '--cifre', type="int", default=0, metavar='N', help="use at least N chars to represents the numbers")
parser.add_option('-u', '--use-dirname', action='store_true', default=False, help="use the dir name instead of the original name file")
options, args = parser.parse_args()

try:
    scarti = set(int(parametro) for parametro in args)
except ValueError:
    raise SystemExit('ci sono elementi che non sono numeri, tra gli scarti')

chdir(options.dir)
filePresenti = sorted(listdir('.'))

associa = []
for file in filePresenti:
    while options.begin in scarti:
        options.begin += 1
    associa.append((file, options.begin))
    options.begin += 1

if options.use_dirname:
    formato = ' - %%.%dd' % max(options.cifre, len(str(associa[-1][1])))
else:
    formato = '%%.%dd - ' % max(options.cifre, len(str(associa[-1][1])))

if options.use_dirname:
    nome_directory = basename(abspath(curdir))

for sorgente, intero in associa:
    if options.use_dirname:
        destinazione = nome_directory + formato % intero + splitext(sorgente)[1] # nb: assicurarsi che l'estensione ci sia :D
    else:
        destinazione = formato % intero + sorgente
    if not exists(destinazione):
        if options.verbose:
            print sorgente, '->', destinazione
        rename(sorgente, destinazione)
    else:
        warn(destinazione+' è già usato!', RuntimeWarning, 2)
