#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Converter for text file from dos/windows to linux
    fondamentally
      * decode from (ASCII|iso-8859-15|cp-1252) to utf8
      * convert CRLF to CR only'''

def mkparser():
    '''"Factory" to create, populate and use an OptionParser istance'''
    from optparse import OptionParser
    parser = OptionParser(version='%prog 0.1', usage='''%prog [FILES]
            convert a (text-only) file from dos to linux''')
    parser.add_option('-b', '--backup', type='string', default='~',
            help='Use BACKUP as backup suffix (default = %default)')
    parser.add_option('-e', '--source-encoding', type='string', default='auto',
            help='Set the source file encoding (default = %default)')
    parser.add_option('-t', '--test', action='store_true', default=False,
            help='Test only (default = %default)')
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help='Show stuff on the STDOUT (default = %default)')
    return parser.parse_args()

def find_encoding(filename):
    '''Use a guesser(?) to find the filename encoding'''
    # TODO: actually find it!
    return 'iso-8859-15'

def main(options, args):
    '''Main script; args is supposed to be a list of file names'''
    from codecs import open as codecs_open
    from shutil import move
    for arg in args:
        infilename = "%s%s" % (arg, options.backup)
        if options.verbose:
            print 'mv %r %r' % (arg, infilename)
        if not options.test:
            move(arg, infilename)
        outfilename = arg
        if options.source_encoding == 'auto':
            encoding = find_encoding(arg)
        else:
            encoding = options.source_encoding
        if options.verbose:
            print 'converting %r (%r) to %r (%r)' % (infilename, encoding,
                    outfilename, 'utf-8')
        if not options.test:
            with codecs_open(infilename, encoding=encoding) as infile:
                with codecs_open(outfilename, 'wb', encoding='utf8') as outfile:
                    outfile.write(infile.read())

if __name__ == '__main__':
    OPTIONS, ARGS = mkparser()
    main(OPTIONS, ARGS)
