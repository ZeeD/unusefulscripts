#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2007-11-04
# Tagga.py

version = '0.1'
formatiSupportati = ('ogg', 'mp3')

from sys import stderr # per warn/1
from optparse import OptionParser
from os.path import isdir, abspath, basename, isfile, join
from os import listdir

def riconosciStruttura(directory):
    """Ritorna Album, Compilation, Singoli o Sconosciuta"""
    # è necessario riconoscere che tipo di struttura ho:
    # Album = ${AUTORE}/${ANNO} - ${ALBUM} - ${N_DISCO}/${N_TRACCIA} - ${TITOLO}.${EXT}
    # Compilation = ${ANNO} - ${ALBUM} - ${N_DISCO}/${N_TRACCIA} - ${AUTORE} - ${TITOLO}.${EXT}
    # Singoli = ${AUTORE}/${ANNO} - ${TITOLO}.${EXT}

    nomeDir = basename(directory)

    try:
        a, b, c = nomeDir.split(' - ')
        int(a)
        int(c)
    except ValueError:
        # può essere Album, Singoli o Sconosciuta
        elements = [join(directory, base) for base in listdir(directory)]
        if all(isdir(element) for element in elements): # sono tutte directory
            # può essere Album o Sconosciuta
            nomeElements = [basename(element) for element in elements]
            for element, nomeElement in zip(elements, nomeElements):
                try:
                    a, b, c = nomeElement.split(' - ')
                    int(a)
                    int(c)
                except ValueError:
                    # è Sconosciuta
                    return 'Sconosciuta'
                nipoti = [join(element, base) for base in listdir(element)]
                if all(isfile(nipote) for nipote in nipoti):
                    nomeNipoti = [basename(nipote) for nipote in nipoti]
                    for nomeNipote in nomeNipoti:
                        try:
                            a, b = nomeNipote.split(' - ')
                            int(a)
                        except ValueError:
                            # è Sconosciuta
                            return 'Sconosciuta'
                        else:
                            if any(b.endswith(ext) for ext in formatiSupportati):
                                # è Album
                                return 'Album'
                            else:
                                # è Sconosciuta
                                return 'Sconosciuta'
                else:
                    # è Sconosciuta
                    return 'Sconosciuta'
        elif all(isfile(element) for element in elements): # sono tutti file
            # può essere Singoli o Sconosciuta
            nomeElements = [basename(element) for element in elements]
            for nomeElement in nomeElements:
                try:
                    a, b = nomeElement.split(' - ')
                    int(a)
                except ValueError:
                    # è Sconosciuta
                    return 'Sconosciuta'
                else:
                    if any(b.endswith(ext) for ext in formatiSupportati):
                        # è Singoli
                        return 'Singoli'
                    else:
                        # è Sconosciuta
                        return 'Sconosciuta'
        else:
            # è Sconosciuta
            return 'Sconosciuta'
    else:
        # può essere Compilation o Sconosciuta
        elements = [join(directory, base) for base in listdir(directory)]
        if all(isfile(element) for element in elements): # sono tutti file
            nomeElements = [basename(element) for element in elements]
            for nomeElement in nomeElements:
                try:
                    a, b, c = nomeElement.split(' - ')
                    int(a)
                except ValueError:
                    # è Sconosciuta
                    return 'Sconosciuta'
                else:
                    if any(c.endswith(ext) for ext in formatiSupportati):
                        # è Singoli
                        return 'Compilation'
                    else:
                        # è Sconosciuta
                        return 'Sconosciuta'
        else:
            # è Sconosciuta
            return 'Sconosciuta'

def album(directory, test, verbose):
    print "Album"

def compilation(directory, test, verbose):
    print "Compilation"

def singoli(directory, test, verbose):
    print "Singoli"

def tagga(directories, test, verbose):
    for directory in directories:
        diz = {'Album': album, 'Compilation': compilation, 'Singoli': singoli,
                'Sconosciuta': lambda directory, test, verbose:
                        warn("`%s' non ha una struttura valida" % directory)}
        diz[riconosciStruttura(directory)](directory, test, verbose)

def warn(string):
    print >> stderr, "Warning:", string

if __name__ == '__main__':
    parser = OptionParser(version='%%prog %s' % version,
            usage='%prog [options] [DIRS...]')
    parser.add_option('-t', '--test', action='store_true', default=False,
            help="effettua solo un test, non sposta i file")
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help="mostra su STDOUT cosa accade (utile con --test)")
    options, args = parser.parse_args()

    if not args:
        directories = [abspath('.')]
    else:
        directories = []
        for arg in args:
            if isdir(arg):
                directories.append(abspath(arg))
            else:
                warn("`%s' non è una directory." % arg)

    tagga(directories, test=options.test, verbose=options.verbose)
