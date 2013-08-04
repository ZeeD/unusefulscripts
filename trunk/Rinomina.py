#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Rinomina.py
-----------

Little script used to rename files in a directory reformatting them in a
sequence, following a series of rules.
'''

from optparse import OptionParser, OptionValueError
from os import chdir, listdir, rename
from os.path import abspath, basename, curdir, exists, splitext, isfile, isdir
from warnings import warn
from Image import open as im_open


def check_dir(option, opt, value, parser):
    '''Input validating function to check if a value it's a directory'''
    # pylint: disable-msg=W0613
    class NotADirectory(OptionValueError):
        '''Wrapper OptionValueError class used to this particular case'''
        pass
    if not isdir(value):
        raise NotADirectory(value)
    parser.values.dir = value


def sort_images(image_file_name):
    '''Regole: una immagine è più grande di un'altra se la sua superficie è
    maggiore. --> x*y deve essere grande
    A parità di superficie, si ritiene maggiore quella più quadrata. --> x == y
    --> abs(x-y) deve -> 0 positivamente --> -abs(x-y) deve -> 0 negativame (e
    più grande è meglio è)
    A parità di diagonale, sono uguali :P'''
    try:
        im_x, im_y = im_open(image_file_name).size
    except Exception as e:
        print(image_file_name)
        raise e
    else:
        return (im_x*im_y, -abs(im_x-im_y))


def mkparser():
    '''create and return an OptionParser instance with all options added'''
    ret = OptionParser(version='%prog 0.3', usage='''%prog [OPTS] [SCRAP|...]
            Rename files with a leading number, except those SCRAP-ped''')
    ret.add_option(
        '-d', '--dir',
        action="callback", type='string', default='.',
        callback=check_dir,
        help="Sort files in DIR (default='%default')")
    ret.add_option(
        '-b', '--begin',
        type="int", default=1, metavar='N',
        help="Start enumerating from N (default=%default)")
    ret.add_option(
        '-v', '--verbose',
        action='store_true', default=False,
        help="Show on STDOUT what happens")
    ret.add_option(
        '-c', '--cifre',
        type="int", default=0, metavar='N',
        help="Use at least N chars to represents the numbers")
    ret.add_option(
        '-u', '--use-dirname',
        action='store_true', default=False,
        help="Use the dir name instead of the original name file")
    ret.add_option(
        '-i', '--imgs',
        action='store_true', default=False,
        help="Files are images: sort then by pixel resolution, not by name")
    ret.add_option(
        '-t', '--test',
        action='store_true', default=False,
        help="Test only: doesn't actually rename anything")
    ret.add_option(
        '-a', '--also-dir',
        action='store_true', default=False,
        help="Rename also the directories (not recursive!)")
    return ret


def parse_and_validate_args():
    '''simple wrapper around mkparser()'''
    parser = mkparser()
    options, args = parser.parse_args()
    scarti = set(int(parametro) for parametro in args)
    return options, scarti


def mk_associations(filenames, begin, scarti):
    '''return a 2-tuple: (dict(source_name: number), max_used_number_length)'''
    associations = {}
    number = begin
    for filename in filenames:
        while number in scarti:
            number += 1
        associations[filename] = number
        number += 1
    return associations, len(str(number-1))


def main():
    '''main function'''
    options, scarti = parse_and_validate_args()
    chdir(options.dir)
    filenames = sorted(
        (
            filename for filename in listdir('.')
            if isfile(filename) or options.also_dir and isdir(filename)
        ),
        key=sort_images if options.imgs else None,
        reverse=options.imgs)

    associa, max_length = mk_associations(filenames, options.begin, scarti)
    max_length = max(options.cifre, max_length)

    if options.use_dirname:
        nome_directory = basename(abspath(curdir))

    fmt = ' - %%.%dd' if options.use_dirname else '%%.%dd - '
    formato = fmt % max_length

    for sorgente, intero in sorted(associa.items()):
        if options.use_dirname:
            ext = splitext(sorgente)[1]     # be sure there is an extension!
            destinazione = nome_directory + formato % intero + ext
        else:
            destinazione = formato % intero + sorgente
        if not exists(destinazione):
            if options.verbose:
                print sorgente, '->', destinazione,
                if options.imgs:
                    im_x, im_y = im_open(sorgente).size
                    print "(%dx%d, %d, %d)" % (
                        im_x, im_y, im_x*im_y,
                        -abs(im_x-im_y)
                    )
                else:
                    print
            if not options.test:
                rename(sorgente, destinazione)
        else:
            warn(destinazione+' è già usato!', RuntimeWarning, 2)

if __name__ == '__main__':
    main()
