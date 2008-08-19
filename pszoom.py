#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2008-07-02 - Permette di usare stdin - TODO: usare optparse
# 2008-06-29
# pszoom.py

from subprocess import Popen, PIPE, STDOUT
from itertools import tee

def calcola_bordi(stream_in, max_numero_pagine=3):
    from os import kill, O_NONBLOCK
    from signal import SIGTERM
    from fcntl import fcntl, F_GETFL, F_SETFL

    popen_gs = Popen(('gs', '-sDEVICE=bbox', '-dBATCH', '-dNOPAUSE', '-q', '-'),
            stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    fcntl(popen_gs.stdout, F_SETFL, fcntl(popen_gs.stdout, F_GETFL) | O_NONBLOCK)

    bordi = (32000, 32000, -32000, -32000)
    i = 0
    for row_in in stream_in:
        if i >= max_numero_pagine:
            kill(popen_gs.pid, SIGTERM)
            break
        if popen_gs.poll() is not None:
            break
        popen_gs.stdin.write(row_in)
        try:
            row_out = popen_gs.stdout.readline()
        except IOError:
            continue
        if row_out.startswith('%%HiResBoundingBox:'):
            tmp = zip(map(float, row_out.split()[1:5]), bordi)
            bordi = map(min, tmp[:2]) + map(max, tmp[2:])
            i += 1
    if (bordi[0] >= bordi[2]) or (bordi[1] >= bordi[3]):
        raise "Errore calcolo bordi"
    return bordi

def effettua_zoom((x0, y0, x1, y1), stream_in, stream_out):
    # 1 inch = 72 punti = 25.40 mm -> 1 mm = 72/25.40 punti
    width, height = map(lambda m: m*72./25.40, (210., 297.)) # di default ho A4
    s1, s2 = tee(stream_in)
    for row in s1:
        if row.startswith('%%BoundingBox:'):
            tmp = map(float, row.split()[1:5])
            width = tmp[2] - tmp[0]
            height = tmp[3] - tmp[1]
            break
    page_spec = "0@%(scale)f(%(xoff)f,%(yoff)f)" % {
        'scale': min(width/(x1-x0), height/(y1-y0)),
        'xoff': -x0,
        'yoff': -y0#-72 # mmm, ma perché c'è questo offset di un pollice???
    }
    popen_pstops = Popen(('pstops', page_spec), stdin=PIPE, stdout=stream_out)
    for row in s2:
        popen_pstops.stdin.write(row)

if __name__ == '__main__':
    from sys import stdin, stdout, argv
    try:
        in1, in2 = tee(open(argv[1]))
    except IndexError:
        in1, in2 = tee(stdin)
    try:
        out = open(argv[2], 'w')
    except IndexError:
        out = stdout

    bordi = calcola_bordi(in1)
    effettua_zoom(bordi, in2, out)
