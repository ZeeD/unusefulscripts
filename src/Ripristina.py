#!/usr/bin/env python3

from optparse import OptionParser
from os import rename


def main():
    option_parser = build_option_parser()
    options, args = option_parser.parse_args()
    output = args[0]

    ripristina(output, options)


def build_option_parser():
    """Create an OptionParser istance, add the user options and return it"""
    parser = OptionParser(version='%prog 0.1', usage='%prog [OPTIONS] OUTPUT')
    parser.add_option(
        '-t',
        '--test',
        action='store_true',
        default=False,
        help="test only: doesn't actually rename anything",
    )
    parser.add_option(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='show on STDOUT what happens',
    )
    parser.add_option(
        '-s',
        '--separator',
        action='store',
        default=' -> ',
        type=str,
        help='imposta il separatore fra il vecchio e il nuovo nome',
    )

    return parser


def ripristina(output, options):
    for row in output.split('\n'):
        old_name, new_name = row.split(options.separator)
        if options.verbose:
            print('mv %r %r;' % (new_name, old_name))
        if not options.test:
            rename(new_name, old_name)


if __name__ == '__main__':
    main()
