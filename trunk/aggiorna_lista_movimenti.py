#!/usr/bin/env python
# -*- coding: utf8 -*-

from sys import stdout

def main(historian_file_name, news_file_name, out_file=stdout):
    ''' mi aspetto i file 'BPOL_ListaMovi.txt' e 'BPOL_ListaMovi(2).txt', con:
     3 righe uguali     (linea vuota, n° conto, intestatari)         +
     3 righe differenti (data saldo, contabile, disponibile)         +
     5 righe uguali     (2 linee vuote, nome colonne, 2 linee vuote) +
    ?? righe aggiunte   (i nuovi movimenti)                          +
    ?? righe uguali     (lo storico dei movimenti in comune)         +
    ?? righe cancellate (che non m'interessano)'''
    with open(historian_file_name) as historian_file:
        historian = historian_file.readlines()
        with open(news_file_name) as news_file:
            news = news_file.readlines()
            for _ in range(3):
                out_file.write(historian.pop(0))    # prendo le 3 righe uguali
                news.pop(0)                         # le levo a entrambi i file
            for _ in range(3):
                historian.pop(0)                    # ignoro le 3 righe vecchie
                out_file.write(news.pop(0))         # prendo le 3 righe nuove
            for _ in range(5):
                out_file.write(historian.pop(0))    # prendo le 5 righe uguali
                news.pop(0)                         # le levo a entrambi i file
            while historian[0] != news[0]:  # finché le righe sono diverse
                out_file.write(news.pop(0)) # stampa le aggiunte
            out_file.writelines(historian)  # stampa le righe rimanenti

if __name__ == '__main__':
    from sys import argv, stderr
    try:
        main(argv[1], argv[2])
    except:
        stderr.write("Usage: %s HISTORIAN NEWS\n")
