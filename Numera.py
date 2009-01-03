#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser, OptionValueError
from os import rename
from os.path import exists, basename, dirname, join, abspath, splitext

def number_len(i):
    """Calcola il numero di cifre necessarie per un numero in una certa base"""
    return len(str(int(i)))

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
    parser.add_option('-u', '--use-dirname', action='store_true', default=False,
            help='Invece del nome originale, usa il nome della directory')
    parser.add_option('-p', '--pre', type=str, default='', metavar='STR',
            help='Inserisci la stringa STR in testa')
    parser.add_option('-s', '--switch', action='store_true', default=False,
            help='Inverti di posizione nome del file e numero (utile con -u)')

    options, args = parser.parse_args()

    max_number = 0
    substitutions = []
    for pos, param in enumerate(args):
        max_number = options.begin + pos
        if param:
            substitutions.append((dirname(param), basename(param), max_number))

    format = '%%.%dd' % max(options.cifre, number_len(max_number))

    for sourcedir, sourcename, number in substitutions:
        source = join(sourcedir, sourcename)
        filename, ext = splitext(sourcename)
        if options.use_dirname:
            filename = basename(abspath(sourcedir))
        if not options.switch:
            completefilename = "%s - %s" % (format % number, filename)
        else:
            completefilename = "%s - %s" % (filename, format % number)
        dest = join(sourcedir, options.pre + completefilename + ext)
        if not exists(dest):
            if options.verbose:
                print source, '->', dest
            if not options.test:
                rename(source, dest)
        else:
            warn(dest + ' è già usato!', RuntimeWarning, 2)
