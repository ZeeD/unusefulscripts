#!/usr/bin/env python

import optparse
import os
import sys


def warn(string, args=()):
    """Comunica warning su stderr, con una sintassi simile a quella di optparse"""
    sys.stderr.write('%s: warning: %s\n' % (sys.argv[0], string % args))


def sistema_case(options, args):
    for parametro in args:
        percorso, vecchioNome = os.path.split(parametro)
        if not vecchioNome:  # se è una directory
            percorso, vecchioNome = os.path.split(percorso)

        vecchioNomeSplittato = vecchioNome.split(' - ')
        nuovoNome = []

        if options.document:
            # il primo elemento contiene nomi propri, quindi capitalizzo tutto
            autori = []
            for autore in vecchioNomeSplittato[0].split():
                autori.append(autore.decode('utf8').capitalize().encode('utf8'))
            nuovoNome.append(', '.join(autori))

        for el in vecchioNomeSplittato[options.document :]:
            nuovoNome.append(el.decode('utf8').capitalize().encode('utf8'))

        nuovoNome = ' - '.join(nuovoNome)

        # per le S.I.G.L.E.
        tmp = nuovoNome.split('.')
        for i, e in enumerate(tmp):
            if not e[-2:-1].isalnum():
                try:
                    tmp[i] = e[:-1] + e[-1].upper()
                except IndexError:
                    tmp[i] = e[:-1]  # per "..."
        nuovoNome = '.'.join(tmp)

        vecchioNome = os.path.join(percorso, vecchioNome)
        nuovoNome = os.path.join(percorso, nuovoNome)
        if os.path.exists(nuovoNome):
            warn('%s è già usato!', nuovoNome)
        else:
            if options.verbose:
                print(f'{vecchioNome} -> {nuovoNome}')
            if not options.test:
                os.rename(vecchioNome, nuovoNome)


def filenames(recursive, args):
    """Generatore di tutti i file da rinominare (utile se recursive=True)"""
    for arg in args:
        if recursive:
            for base, dirs, files in os.walk(arg, topdown=False):
                for file_ in files:
                    yield os.path.join(base, file_)
                for dir_ in dirs:
                    yield os.path.join(base, dir_)
        yield arg


class OptionParser(optparse.OptionParser):
    def check_values(self, values, args):
        """Controlla se c'è almeno un parametro e che tutti corrispondano a file"""
        if not args:
            self.error('Devi definire almeno un file da rinominare!')
        for arg in args:
            if not os.path.exists(arg):
                self.error("File non trovato: `%s'" % arg)
        return optparse.OptionParser.check_values(self, values, args)


if __name__ == '__main__':
    parser = OptionParser(version='%prog 0.7', usage='%prog FILE...')
    parser.add_option(
        '-d',
        '--document',
        action='store_true',
        help='Modalità per documenti (Nome Cognome - Documento.ext)',
    )
    parser.add_option(
        '-v',
        '--verbose',
        action='store_true',
        help='Mostra su STDOUT le azioni compiute',
    )
    parser.add_option(
        '-t',
        '--test',
        action='store_true',
        help="Non compiere nessuna rinomina (utile con '--verbose')",
    )
    parser.add_option(
        '-r',
        '-R',
        '--recursive',
        action='store_true',
        help='Agisci in modo ricorsivo anche nelle sotto-directory',
    )
    options, args = parser.parse_args()

    sistema_case(options, filenames(options.recursive, args))
