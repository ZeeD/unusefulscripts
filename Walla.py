#!/usr/bin/env python

'Scan for files and directories searching for (and renaming) wallpaper images'

OUTDIR = '/media/iomegaZeD/Immagini/Wallpaper'
RISOLUZIONI_ACCETTATE = (
    (640,480), (800,600), (1024,768), (1280,960), (1600,1200), (1920,1440),# 4:3
    (1280,800), (1280,1024), (1440,900), (1680,1050), (1920,1080)	# altre
)

from optparse import OptionParser, OptionValueError
from os import listdir, remove, symlink
from os.path import (abspath, basename, dirname, exists, isdir, isfile, islink,
                     join, realpath, split)
from shutil import copy, move

from PIL.Image import open as iopen


def walla_unwalla(directories, files, options):
    '''Recursively tag or untag image files'''
    for directory in directories:
        for filename in (join(directory, f) for f in listdir(directory)):
            if isfile(filename):
                if options.unwall:
                    unwalla_file(filename, options)
                else:
                    walla_file(filename, options)
            else:
                warn("`%s' non è un file. `%s' dovrebbe avere solo immagini.",
                        (filename, directory))
    for filename in files:
        if options.unwall:
            unwalla_file(filename, options)
        else:
            walla_file(filename, options)

def walla_file(filename, options):
    '''Tag a file if it's an image and a wallpaper'''
    try:
        image = iopen(filename)
    except IOError:
        return warn("`%s' non è un'immagine.", filename)

    size = image.size
    if options.verbose:
        print("`%s' -> `%s'" % (filename, size))
    if size not in RISOLUZIONI_ACCETTATE:
        return warn("`%s' non è un wallpaper.", filename)

    base, nome_file = split(filename)
    if options.phase_1:
        output_file = '%s/%sx%s%s - %s' % ((base, ) + size + (" - %s" %
                split(base)[1] if options.add_dirname else "", nome_file))
    elif options.phase_2:
        output_file = join(OUTDIR, nome_file)
    else:
        output_file = join(OUTDIR, '%sx%s%s - %s' % (size + (" - %s" %
                split(base)[1] if options.add_dirname else "", nome_file)))

    if exists(output_file):
        return warn("`%s' è già esistente.", output_file)

    if options.verbose:
        print("\t-> `%s'" % (output_file, ))
    if not options.test:
        if not options.copy:
            move(filename, output_file)
            if options.link:
                symlink(output_file, filename)
        else:
            copy(filename, output_file)

def unwalla_file(input_file_name, options):
    '''Remove the tag from an input file name'''
    try:
        iopen(input_file_name)
    except IOError:
        return warn("`%s' non è un'immagine.", input_file_name)

    root_input_file_name = dirname(input_file_name)
    if islink(input_file_name):
        real_file_name = realpath(input_file_name)
        if options.verbose:
            print("`%s' -> (None)" % input_file_name)
        if not options.test:
            remove(input_file_name)
    else:
        real_file_name = input_file_name

    nome_file = split(real_file_name)[1]
    output_file_name = join(root_input_file_name, ' - '.join(
            nome_file.split(' - ')[1:]))
    if exists(output_file_name):
        return warn("`%s' è già esistente.", output_file_name)

    if options.verbose:
        print("`%s' -> `%s'" % (real_file_name, output_file_name))
    if not options.test:
        move(real_file_name, output_file_name)

def warn(string, args=(), fatal=False):
    '''Warning / Error message generator'''
    from sys import stderr
    stderr.write("%s: %s\n" % ("Error" if fatal else "Warning", string % args))
    if fatal:
        raise SystemExit(fatal)

def set_output_dir(value):
    '''Change the OUTDIR global variable from the script at runtime'''
    if not isdir(value):
        warn("`%s' non è una directory!", value, fatal=True)

    from sys import argv
    with open(argv[0], 'r') as infile:
        temp = ('OUTDIR = %r\n' % (value, ) if line.startswith('OUTDIR') else
                line for line in infile)

    with open(argv[0], 'w') as outfile:
        outfile.writelines(temp)

    raise SystemExit()

def check_is_false(*attributes):
    '"Functional" returning a closure checking if any attribute is already set'
    def callback(option, _opt_str, _value, parser):
        '''Real closure-like callback function'''
        for attribute in attributes:
            if getattr(parser.values, attribute):
                raise OptionValueError("Non puoi settare %s se hai già "
                        "impostato %s" % (option.dest, attribute))
        setattr(parser.values, option.dest, True)
    return callback

def renew(options, args):
    '''Try to find / replace broken symbolic links'''
    from os import readlink
    for arg in args:
        if not islink(arg):
            warn("`%s' non è un link simbolico!", arg)
            continue
        old_path = readlink(arg)
        if isfile(old_path):
            warn("`%s' non è un link simbolico *rotto*!", arg)
            continue
        new_path = join(OUTDIR, basename(old_path))
        if options.verbose:
            print("`%s' -> (None)" % old_path)
        if not options.test:
            remove(arg)
        if options.verbose:
            print("`%s' -> `%s'" % (arg, new_path))
        if not options.test:
            symlink(new_path, arg)
    raise SystemExit()

def known_resolutions(_option, _optstr, _value, _parser):
    """Mostra le risoluzioni riconosciute, ed esce dal programma"""
    raise SystemExit(','.join('%sx%s' % r for r in RISOLUZIONI_ACCETTATE))

def main():
    '''main function'''
    parser = OptionParser(version='%prog 0.5', usage="%prog [options] [DIRS='.'"
            "|FILES]")
    parser.add_option('-l', '--link', action='callback', default=False,
            dest='link', callback=check_is_false('copy'), help="crea anche dei "
                    "link simbolici nelle posizioni originarie")
    parser.add_option('-t', '--test', action='store_true', default=False,
            help="effettua solo un test, non sposta i file")
    parser.add_option('-u', '--unwall', action='store_true', default=False,
            help="ritorna ai valori originari")
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help="mostra su STDOUT cosa accade (utile con --test)")
    parser.add_option('-a', '--add-dirname', action='callback', default=False,
            dest='add_dirname', callback=check_is_false('phase_2'),
            help="aggiunge il nome della directory nel nome del file di output")
    parser.add_option('-s', '--set-output-dir', action='store', default=None,
            dest='OUTDIR', type=str, help="imposta una nuova directory di "
                    "output (corrente = `%s')" % OUTDIR)
    parser.add_option('-c', '--copy', action='callback', default=False,
            dest='copy', callback=check_is_false('link'), help="copia i file, "
                    "invece di spostarli")
    parser.add_option('-1', '--phase-1', action='callback', default=False,
            dest='phase_1', callback=check_is_false('phase_2'), help="formatta "
                    "i file nella directory corrente")
    parser.add_option('-2', '--phase-2', action='callback', default=False,
            dest='phase_2', callback=check_is_false('phase_1', 'add_dirname'),
            help="sposta i file nella directory remota")
    parser.add_option('-r', '--renew', action='store_true', default=False,
            help='Aggiorna dei vecchi link simbolici alla nuova walldir')
    parser.add_option('-k', '--known-resolutions', action='callback',
            callback=known_resolutions, help="Mostra le risoluzioni accettate")
    options, args = parser.parse_args()

    if options.OUTDIR:
        set_output_dir(options.OUTDIR)

    if options.renew:
        renew(options=options, args=(args if args else sorted(listdir('.'))))

    if not args:
        walla_unwalla(directories=[abspath('.')], files=[], options=options)
    else:
        directories = []
        files = []
        for arg in args:
            if isdir(arg):
                directories.append(abspath(arg))
            elif isfile(arg):
                files.append(abspath(arg))
            else:
                warn("`%s' non è né un file né una directory.", arg)
        walla_unwalla(directories=directories, files=files, options=options)

if __name__ == '__main__':
    main()
