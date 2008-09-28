#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser, OptionValueError
from os import chdir, listdir, rename
from os.path import abspath, basename, curdir, exists, splitext, isfile
from warnings import warn
from Image import open

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
parser.add_option('-d', '--dir', action="callback", type='string', default='.',
        callback=check_dir, help="enumerate files located in DIR (default='.')")
parser.add_option('-b', '--begin', type="int", default=1, metavar='N',
        help="start to enumerate from N (default=1)")
parser.add_option('-v', '--verbose', action='store_true', default=False,
        help="show on STDOUT what happens")
parser.add_option('-c', '--cifre', type="int", default=0, metavar='N',
        help="use at least N chars to represents the numbers")
parser.add_option('-u', '--use-dirname', action='store_true', default=False,
        help="use the dir name instead of the original name file")
parser.add_option('-i', '--imgs', action='store_true', default=False,
        help="treat files as images, sort then by pixel resolution, not name")
parser.add_option('-t', '--test', action='store_true', default=False,
        help="test only: doesn't actually rename anything")
options, args = parser.parse_args()

try:
    scarti = set(int(parametro) for parametro in args)
except ValueError:
    raise SystemExit('ci sono elementi che non sono numeri, tra gli scarti')

def sort_images(image_file_name):
    """Regole: una immagine è più grande di un'altra se la sua superficie è più
    grande. --> x*y deve essere grande
    A parità di superficie, si ritiene maggiore quella più quadrata. --> x == y
    --> abs(x-y) deve -> 0 positivamente --> -abs(x-y) deve -> 0 negativame (e
    più grande è meglio è)
    A parità di diagonale, sono uguali :P
    """
    x, y = open(image_file_name).size
    return (x*y, -abs(x-y))

chdir(options.dir)
filePresenti = sorted(filter(isfile, listdir('.')), key=sort_images if
        options.imgs else None, reverse=options.imgs)

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
            print sorgente, '->', destinazione,
            if options.imgs:
                x, y = open(sorgente).size
                print "(%dx%d, %d, %d)" % (x, y, x*y, -abs(x-y))
            else:
                print
        if not options.test:
            rename(sorgente, destinazione)
    else:
        warn(destinazione+' è già usato!', RuntimeWarning, 2)
