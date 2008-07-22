#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 200-06-14 - Versione iniziale
# SistemaNumeri.py

from os.path import exists, split, join
from itertools import starmap, imap, izip

def warn(string, error=False):
    """Comunicazione di warning / errori, con terminazione del programma
    @param string causa del warning / errore
    @param error se è vero, allora è un errore, e termina il programma
    """
    from sys import stderr
    if error:
        stderr.write("Error: `%s'\n" % string)
        raise SystemError
    else:
        stderr.write("Warning: `%s'\n" % string)


def exists_warn(path):
    """Variante di os.path.exists, con warning per l'utente
    @param path percorso del quale verificare l'esistenza
    @see warn()
    """
    return_value = exists(path)
    if not return_value:
        warn("`%s' doesn't exist!" % path)
    return return_value

def find_integers(string):
    """Da una stringa, ritorna una tupla composta da stringhe e interi alternati
    Voglio che ci sia sempre una stringa (anche vuota) in testa; in questa
    implementazione c'è una stringa anche in coda
    @param string stringa
    @return tupla, i cui elementi sono dati da una stringhe e numeri alternati

    >>> find_integers('')   # ritorna sempre una tupla con almeno un elemento
    ('', )
    >>> find_integers('a')  # se c'è solo una stringa, sarà l'unico elemento
    ('a',)
    >>> find_integers('1')  # se c'è solo un numero, sarà preceduto da ''
    ('', 1)
    >>> find_integers('a1') # se c'è già una stringa, saranno solo 2 elementi
    ('a', 1)
    >>> find_integers('1a') # qui no, saranno tre (inizia per numero)
    ('', 1, 'a')
    >>> find_integers('abc123def456')   # lo voglio greedy
    ('abc', 123, 'def', 456)
    """
    out = []
    begin = end = 0
    string_len = len(string)
    while end < string_len:
        if string[end].isdigit():
            out.append(string[begin:end])
            begin = end
            while end < string_len and string[end].isdigit():
                end += 1
            out.append(int(string[begin:end]))
            begin = end
        end += 1
    out.append(string[begin:end])
    return tuple(out)

find_integers2 = lambda s: (('', ) if not s or s[0].isdigit() else ()) + tuple(
    int(''.join(b)) if a else ''.join(b) for a, b in groupby(s, str.isdigit))

def find_integers3(string):
    if not string:
        return ('', )
    ret = []
    if string[0].isdigit():
        ret.append('')
    for is_digit, it in groupby(string, str.isdigit):
        value = ''.join(it)
        if is_digit:
            value = int(value)
        ret.append(value)
    return tuple(ret)

def multi_max(matrix):
    """Data una matrice di valori (rappresentata da una tupla di tuple), ritorna
    la lista dei valori massimi calcolati per le colonne dispari.
    matrix = (
        (Stringa, Numero, Stringa, Numero, Stringa),
        (Stringa, Numero, Stringa),
        (Stringa, Numero, Stringa, Numero, Stringa, Numero, Stringa)...
    )
    return = [Numero, Numero, Numero]
    so che ogni elemento di matrix è una tupla trovata da find_integers!
    """
    out = []
    for row in matrix:
        for index, number in enumerate(row[1::2]):
            try:
                current_max = out[index]
            except IndexError:
                out.append(number)  # sarà di sicuro un off-by-one, non di più
            else:
                if number > current_max:
                    out[index] = number
    return out

def numero_cifre(intero):
    """ritorna il numero di cifre usate nell'intero (in base 10...)"""
    from math import log10
    if intero == 0:
        return 1
    return int(log10(intero) + 1)

def rinomina(tupla, cifre_necessarie):
    """Trasforma una tupla del tipo (Stringa, Intero, Stringa...) in una
    stringa usando per ogni intero un elemento di cifre_necessarie
    """
    ret = [ tupla[0] ]
    i = 0
    while True:
        try:
            numero = tupla[2*i+1]
        except IndexError:
            break
        cifra = cifre_necessarie[i]
        stringa = tupla[2*i+2]
        ret.append("%0*d%s" % (cifra, numero, stringa))
        i += 1
    return ''.join(ret)

def move(options):
    from shutil import move as shmove
    def move_opted(file_from, file_to):
        if options.verbose:
            print file_from, '->', file_to
        if exists(file_to):
            warn("%s è già usato!" % file_to)
        else:
            if not options.test:
                shmove(file_from, file_to)
    return move_opted

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(version='%prog 0.1', usage='''%prog FILE...
    Rinomina i file effettuando il padding dei numeri incontrati''')
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help="Mostra su STDOUT le azioni compiute")
    parser.add_option('-t', '--test', action='store_true', default=False,
            help="Non compiere nessuna rinomina (utile con '--verbose')")

    options, args = parser.parse_args()
    filenames = filter(exists_warn, args)   # filenames è usato 2 volte
    bases, names = izip(*imap(split, filenames))
    names_with_integers = map(find_integers, names) # names_with_integers è usato 2 volte
    cifre_necessarie = map(numero_cifre, multi_max(names_with_integers))    # cifre_necessarie è usato un numero imprecisato di volte!
    re_names = (rinomina(n, cifre_necessarie) for n in names_with_integers)
    destnames = starmap(join, izip(bases, re_names))
    tuple(starmap(move(options), izip(filenames, destnames)))
