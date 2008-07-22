#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2008-06-14 - Supporto per le opzioni '-d', '-t' e '-v'
# 2007-12-09 - Supporto per i nomi di relazioni --> 'Autore[, Autore]* - Titolo.(ps|pdf)'
# 2007-07-16 - OptionParser + patch filename in utf-8
# 2007-05-18 - versione in utf-8
# 2006-10-23 - patch per "..."
# 2006-04-08
# SistemaCase.py

from optparse import OptionParser
from os.path import split, join
from os import access, rename, F_OK
from sys import stderr

def warn(string, args=()):
    print >> stderr, "Warning:", string % args

if __name__ == '__main__':
    parser = OptionParser(version='%prog 0.6', usage='%prog FILE...')
    parser.add_option('-d', '--document', action='store_true', default=False,
            help=u"Usa la modalità per documenti (Nome Cognome - Documento.ext)")
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help="Mostra su STDOUT le azioni compiute")
    parser.add_option('-t', '--test', action='store_true', default=False,
            help="Non compiere nessuna rinomina (utile con '--verbose')")

    options, args = parser.parse_args()
    for parametro in args:
        percorso, vecchioNome = split(parametro)
        if not vecchioNome: # se è una directory
            percorso, vecchioNome = split(percorso)

        vecchioNomeSplittato = vecchioNome.split(' - ')
        nuovoNome = []

        if options.document:
            # il primo elemento contiene nomi propri, quindi capitalizzo tutto
            autori = []
            for autore in vecchioNomeSplittato[0].split():
                autori.append(autore.decode('utf8').capitalize().encode('utf8'))
            nuovoNome.append(', '.join(autori))

        for el in vecchioNomeSplittato[1:] if options.document else vecchioNomeSplittato:
            nuovoNome.append(el.decode('utf8').capitalize().encode('utf8'))

        nuovoNome = ' - '.join(nuovoNome)

        # per le S.I.G.L.E.
        tmp = nuovoNome.split('.')
        for i, e in enumerate(tmp):
            if not e[-2:-1].isalnum():
                try:
                    tmp[i] = e[:-1] + e[-1].upper()
                except IndexError:
                    tmp[i] = e[:-1] # per "..."
        nuovoNome = '.'.join(tmp)

        vecchioNome = join(percorso, vecchioNome)
        nuovoNome = join(percorso, nuovoNome)
        if access(nuovoNome, F_OK):
            warn("%s è già usato!", nuovoNome)
        else:
            if options.verbose:
                print vecchioNome, '->', nuovoNome
            if not options.test:
                rename(vecchioNome, nuovoNome)
