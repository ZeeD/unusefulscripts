#!/usr/bin/env python
# -*- coding: utf8 -*-

from optparse import OptionParser
from os import remove, rename
from os.path import isfile
from sys import argv, stderr

historian_file_name = '/media/iomegaZeD/Lista movimenti bancoposta'

def set_historian(option, opt, value, parser):
    if not isfile(value):
        parser.error("`%s' non è un file!" % value)
    with file(argv[0]) as my_file:
        temp = []
        for line in my_file:
            if line.startswith('historian_file_name'):
                temp.append("historian_file_name = %r\n" % value)
            else:
                temp.append(line)
    with file(argv[0], 'w') as my_file:
        my_file.writelines(temp)
    raise SystemExit

def aggiorna_lista_movimenti(news_file, options):
    ''' mi aspetto che tra lo historian_file e news_file ci siano:
     3 righe uguali     (linea vuota, n° conto, intestatari)         +
     3 righe differenti (data saldo, contabile, disponibile)         +
     5 righe uguali     (2 linee vuote, nome colonne, 2 linee vuote) +
    ?? righe aggiunte   (i nuovi movimenti)                          +
    ?? righe uguali     (lo storico dei movimenti in comune)         +
    ?? righe cancellate (che non m'interessano)'''
    news = news_file.readlines()
    out = []
    with file(historian_file_name) as historian_file:
        historian = historian_file.readlines()
        for _ in range(3):
            hist_line = historian.pop(0)
            news_line = news.pop(0)
            assert hist_line == news_line   # me le aspetto uguali ^^
            if options.verbose:
                stderr.write(' %s' % hist_line)
            out.append(hist_line)
        for _ in range(3):
            hist_line = historian.pop(0)
            news_line = news.pop(0)
            if options.verbose:
                stderr.write('-%s' % hist_line)
                stderr.write('+%s' % news_line)
            out.append(news_line)
        for _ in range(5):
            hist_line = historian.pop(0)
            news_line = news.pop(0)
            assert hist_line == news_line   # me le aspetto uguali ^^
            if options.verbose:
                stderr.write(' %s' % hist_line)
            out.append(hist_line)
        while historian and news and historian[0] != news[0]:   # nuove aggiunte
            news_line = news.pop(0)
            if options.verbose:
                stderr.write('+%s' % news_line)
            out.append(news_line)
        while historian:                    # storico
            hist_line = historian.pop(0)
            if options.verbose:
                stderr.write(' %s' % hist_line)
            out.append(hist_line)
    if options.backup:
        if options.verbose:
            stderr.write('mv %s %s\n' % (historian_file_name, options.backup))
        if not options.test:
            rename(historian_file_name, options.backup)
    if not options.test:
        with file(historian_file_name, 'w') as historian_file:
            historian_file.writelines(out)

if __name__ == '__main__':
    parser = OptionParser(version='%prog 0.1', usage='%prog [OPTIONS] NEWS')
    parser.add_option('-s', '--set-historian', callback=set_historian, type=str,
            metavar='FILE', action='callback', help='imposta un nuovo file per '
            "lo storico (corrente = `%s')" % historian_file_name)
    parser.add_option('-t', '--test', action='store_true', help='Non effettuare'
            " modifiche (utile con '--verbose')")
    parser.add_option('-b', '--backup', action='store', metavar="FILE",
            default=None, help='crea FILE come copia di backup')
    parser.add_option('-v', '--verbose', action='store_true', help='Mostra su '
            'STDOUT le azioni compiute')
    parser.add_option('-c', '--clear', action='store_true', help='Cancella il '
            'file degli aggiornamenti alla fine delle operazioni')
    options, args = parser.parse_args()

    if len(args) < 1:
        raise SystemExit(parser.print_usage())

    with file(args[0]) as news_file:
        aggiorna_lista_movimenti(news_file, options)
    if options.clear:
        if options.verbose:
            stderr.write('rm -f %s\n' % args[0])
        if not options.test:
            remove(args[0])
