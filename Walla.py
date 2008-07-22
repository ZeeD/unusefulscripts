#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2008-05-04 - aggiunte le opzioni '--current-dir' e '--set-output-dir',
#              ripulitura generale
# 2008-03-16 - aggiunti altri formati supportati (1920x1440)
# 2007-12-26 - aggiunti altri formati supportati (1440x900)
# 2007-07-16 - unWall
# 2007-07-13 - versione in utf-8
# 2006-09-17
# Walla2.py

outDir = '/media/iomegaZeD/Immagini/Wallpaper'
risoluzioniAccettate = (
    (640,480), (800,600), (1024,768), (1280,960), (1600,1200), (1920,1440),# 4:3
    (1280,800), (1280,1024), (1440, 900)                                 # altre
)

from optparse import OptionParser
from os.path import isdir, isfile, basename, abspath, join, split, exists, \
        islink, realpath, dirname
from sys import stderr, exit
from os import listdir, symlink, remove
from Image import open
from shutil import move

def walla_unwalla(directories, files):
    for directory in directories:
        for file in listdir(directory):
            file = join(directory, file)
            if isfile(file):
                if options.unwall:
                    unwallaFile(file)
                else:
                    wallaFile(file)
            else:
                warn("`%s' non è un file. `%s' dovrebbe avere solo immagini.",
                        (file, directory))
    for file in files:
        if options.unwall:
            unwallaFile(file)
        else:
            wallaFile(file)

def wallaFile(file):
    try:
        image = open(file)
    except IOError:
        warn("`%s' non è un'immagine.", file)
    else:
        size = image.size
        if options.verbose:
            print "`%s' -> `%s'" % (file, size)
        if size not in risoluzioniAccettate:
            warn("`%s' non è un wallpaper.", file)
        else:
            base, nomeFile = split(file)
            if options.add_dirname:
                dir_name = split(base)[1]
                outputFile = join(outDir, '%sx%s - %s - %s' % (size + (dir_name,
                        nomeFile)))
            else:
                outputFile = join(outDir, '%sx%s - %s' % (size + (nomeFile, )))
            if exists(outputFile):
                warn("`%s' è già esistente.", outputFile)
            else:
                if options.verbose:
                    print "\t-> `%s'" % (outputFile, )
                if not options.test:
                    move(file, outputFile)
                    if options.link:
                        symlink(outputFile, file)

def unwallaFile(inputFileName):
    try:
        open(inputFileName)
    except IOError:
        warn("`%s' non è un'immagine.", inputFileName)
    else:
        rootInputFileName = dirname(inputFileName)
        if islink(inputFileName):
            realFileName = realpath(inputFileName)
            if options.verbose:
                print "`%s' -> (None)" % inputFileName
            if not options.test:
                remove(inputFileName)
        else:
            realFileName = inputFileName
        base, nomeFile = split(realFileName)
        outputFileName = join(rootInputFileName,
                ' - '.join(nomeFile.split(' - ')[1:]))
        if exists(outputFileName):
            warn("`%s' è già esistente.", outputFileName)
        else:
            if options.verbose:
                print "`%s' -> `%s'" % (realFileName, outputFileName)
            if not options.test:
                move(realFileName, outputFileName)

def warn(string, args=(), fatal=False):
    print >> stderr, "Warning:", string % args
    if fatal:
        exit(fatal)

def set_output_dir(option, opt, value, parser):
    if not isdir(value):
        warn("Errore! `%s' non è una directory!", value, fatal=True)
    from sys import argv
    temp = []
    for line in file(argv[0], 'r'):
        if line.startswith("outDir"):
            temp.append("%s = %r\n" % ("outDir", value))
        else:
            temp.append(line)
    file_out = file(argv[0], 'w')
    file_out.writelines(temp)
    file_out.close()
    exit()

if __name__ == '__main__':
    parser = OptionParser(version='%prog 0.3',
            usage="%prog [options] [DIRS='.'|FILES]")
    parser.add_option('-l', '--link', action='store_true', default=False,
            help="dopo aver spostato i file, crea dei link simbolici nelle \
posizioni originarie")
    parser.add_option('-t', '--test', action='store_true', default=False,
            help="effettua solo un test, non sposta i file")
    parser.add_option('-u', '--unwall', action='store_true', default=False,
            help="ritorna ai valori originari")
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help="mostra su STDOUT cosa accade (utile con --test)")
    parser.add_option('-a', '--add-dirname', action='store_true', default=False,
            help="""aggiunge il nome della directory come prefisso al file di \
output""")
    parser.add_option('-s', '--set-output-dir', action='callback', type=str,
            callback=set_output_dir, help="""Imposta una nuova directory di \
output (corrente = `%s')""" % outDir)
    parser.add_option('-c', '--current-dir', action='store_true', default=False,
            help="Rinomina i files nella directory corrente")
    options, args = parser.parse_args()

    if options.current_dir:
        outDir = ''

    if not args:
        walla_unwalla(directories=[abspath('.')], files=[])
    else:
        directories=[]
        files=[]
        for arg in args:
            if isdir(arg):
                directories.append(abspath(arg))
            elif isfile(arg):
                files.append(abspath(arg))
            else:
                warn("`%s' non è né un file né una directory.", arg)
        walla_unwalla(directories=directories, files=files)
