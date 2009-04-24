#!/usr/bin/env python

from urllib import urlencode, urlopen, urlretrieve
from re import compile

allowed_styles = frozenset(('default', 'earth', 'modern-blue', 'mscgen',
        'omegapple', 'qsd', 'rose', 'roundgreen', 'napkin'))

def getSequenceDiagram(text, outputFile, style='default'):
    wsd = 'http://www.websequencediagrams.com/'
    f = urlopen(wsd, urlencode({ 'message': text, 'style': style }))
    m = compile('(\?img=\w+)').search(f.readline())
    f.close()
    urlretrieve('/'.join((wsd, m.group(0))), outputFile)

def list_styles(self, opt, value, parser, *args, **kwargs):
    raise SystemExit('\n'.join(sorted(allowed_styles)))

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(version='%prog 0.1', usage='%prog [sequence-diagram]')
    parser.add_option('-s', '--style', action='store', default='default',
            help='Set the style (default=%default)')
    parser.add_option('-l', '--list-styles', action='callback', default=None,
            callback=list_styles, help='List allowed styles')
    parser.add_option('-o', '--output-file', action='store', default='out.png',
            help='Set the output file (default=%default)')
    options, args = parser.parse_args()
    if not args:
        from sys import stdin
        sequence_source = stdin
    else:
        sequence_source = open(args[0])
    getSequenceDiagram(sequence_source.read(), options.output_file,
            options.style)
