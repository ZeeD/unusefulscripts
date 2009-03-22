#!/usr/bin/env python
# -*- coding: utf8 -*-

from optparse import OptionParser
from os import remove, rename
from os.path import isfile
from sys import argv, stderr

historian_file_name = '/media/iomegaZeD/Lista movimenti postepay'

def valid_input_data(data):
    expected_output = """Carta Poste Pay n.: 4023600471304149
Intestatario: DE TULLIO VITO
SALDO AL    SALDO CONTABILE (euro)  SALDO DISPONIBILE (euro)
DATA CONTABILE  DATA VALUTA ADDEBITI
(euro)  ACCREDITI
(euro)  DESCRIZIONE OPERAZIONI
Nuova ricerca
"""
    data_output = ''.join(data[:3]+data[4:7]+data[-1:])
    print "%r" % data_output
    print "%r" % expected_output
    return expected_output == data_output

def aggiorna_lista_postepay(news_file, options):
    '''no docstring'''
    # Mi aspetto che news_file sia un file di testo di cui
    # le righe <= 12 siano inutili
    # le righe <= 26 (dal fondo) siano inutili
    data = news_file.readlines()[12:-26]
    assert valid_input_data(data), "`%s': file non valido" % news_file.name
    # Mi aspetto di avere, adesso:
    #  3 righe uguali       (N° carta, Intestatario, Header saldo)  +
    #  1 riga differente    (ultimo saldo)                          +
    #  3 righe uguali       (header dettagli)                       +
    # ?? righe diverse      (nuove operazioni)                      +
    # ?? righe uguali       (operazioni in comune)                  +
    # ?? righe diverse      (vecchie operazioni)
    out = []
    with file(historian_file_name) as historian_file:
        historian = historian_file.readlines()
        for _ in range(3):
            line = historian.pop(0)
            assert line == data.pop(0)
            if options.verbose:
                stderr.write(' %s' % line)
            out.append(line)
        old_line = historian.pop(0)
        new_line = data.pop(0)
        if old_line == new_line:    # storico già aggiornato!
            raise SystemExit("Il file è già aggiornato all'ultima versione")
        if options.verbose:
            stderr.write('-%s' % old_line)
            stderr.write('+%s' % new_line)
        out.append(new_line)
        for _ in range(3):
            line = historian.pop(0)
            assert line == data.pop(0)
            if options.verbose:
                stderr.write(' %s' % line)
            out.append(line)
        while data and (not historian or historian[0] != data[0]): # nuovi movimenti
            new_line = data.pop(0)
            if options.verbose:
                stderr.write('+%s' % new_line)
            out.append(new_line)
        while historian:                                      # vecchi movimenti
            hist_line = historian.pop(0)
            if options.verbose:
                stderr.write(' %s' % hist_line)
            out.append(hist_line)
    if options.backup:
        if options.verbose:
            stderr.write('mv %r %r\n' % (historian_file_name, options.backup))
        if not options.test:
            rename(historian_file_name, options.backup)
    if not options.test:
        with file(historian_file_name, 'w') as historian_file:
            historian_file.writelines(out)

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
        aggiorna_lista_postepay(news_file, options)
    if options.clear:
        if options.verbose:
            stderr.write('rm -f %r\n' % args[0])
        if not options.test:
            remove(args[0])
