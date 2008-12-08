#!/usr/bin/env python
# -*- coding: utf-8 -*-

outDir = '/media/iomegaZeD/Immagini/Wallpaper'
risoluzioniAccettate = (
    (640,480), (800,600), (1024,768), (1280,960), (1600,1200), (1920,1440),# 4:3
    (1280,800), (1280,1024), (1440, 900)                                 # altre
)

from optparse import OptionParser, OptionValueError
from os.path import isdir, isfile, basename, abspath, join, split, exists, \
        islink, realpath, dirname
from sys import stderr, exit
from os import listdir, symlink, remove
from Image import open
from shutil import move, copy

def walla_unwalla(directories, files):
    for directory in directories:
        for file in (join(directory, f) for f in listdir(directory)):
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
            if options.phase_1:
                outputFile = '%s/%sx%s%s - %s' % ((base, ) + size + (" - %s" %
                        split(base)[1] if options.add_dirname else "", nomeFile
                        ))
            elif options.phase_2:
                outputFile = join(outDir, nomeFile)
            else:
                outputFile = join(outDir, '%sx%s%s - %s' % (size + (" - %s" %
                        split(base)[1] if options.add_dirname else "", nomeFile
                        )))
            if exists(outputFile):
                warn("`%s' è già esistente.", outputFile)
            else:
                if options.verbose:
                    print "\t-> `%s'" % (outputFile, )
                if not options.test:
                    if not options.copy:
                        move(file, outputFile)
                        if options.link:
                            symlink(outputFile, file)
                    else:
                        copy(file, outputFile)

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
    print >> stderr, "Warning:" if not fatal else "Error:", string % args
    if fatal:
        exit(fatal)

def set_output_dir(value):
    if not isdir(value):
        warn("`%s' non è una directory!", value, fatal=True)
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

def check_is_false(attributes):
    def callback(option, opt_str, value, parser):
        for attribute in attributes:
            if getattr(parser.values, attribute):
                raise OptionValueError("Non puoi settare %s se hai già "
                        "impostato %s" % (option.dest, attribute))
        setattr(parser.values, option.dest, True)
    return callback

if __name__ == '__main__':
    parser = OptionParser(version='%prog 0.4', usage="%prog [options] [DIRS='.'"
            "|FILES]")
    parser.add_option('-l', '--link', action='callback', default=False,
            dest='link', callback=check_is_false(('copy', )), help="crea dei "
            "link simbolici nelle posizioni originarie")
    parser.add_option('-t', '--test', action='store_true', default=False,
            help="effettua solo un test, non sposta i file")
    parser.add_option('-u', '--unwall', action='store_true', default=False,
            help="ritorna ai valori originari")
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help="mostra su STDOUT cosa accade (utile con --test)")
    parser.add_option('-a', '--add-dirname', action='callback', default=False,
            dest='add_dirname', callback=check_is_false(('phase_2', )),
            help="aggiunge il nome della directory nel nome del file di output")
    parser.add_option('-s', '--set-output-dir', action='store', default=None,
            dest='outDir', type=str, help="imposta una nuova directory di "
            "output (corrente = `%s')" % outDir)
    parser.add_option('-c', '--copy', action='callback', default=False,
            dest='copy', callback=check_is_false(('link', )), help="copia i "
            "file, invece di spostarli")
    parser.add_option('-1', '--phase-1', action='callback', default=False,
            dest='phase_1', callback=check_is_false(('phase_2', )),
            help="formatta i file nella directory corrente")
    parser.add_option('-2', '--phase-2', action='callback', default=False,
            dest='phase_2', callback=check_is_false(('phase_1', 'add_dirname')),
            help="sposta i file nella directory remota")
    options, args = parser.parse_args()

    if options.outDir:
        set_output_dir(options.outDir)

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
