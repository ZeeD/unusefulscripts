#!/usr/bin/env python

from PIL import Image
from os.path import join, basename
from os import mkdir

def parse_options():
    """Create an OptionParser istance, add the user options and return it"""
    from optparse import OptionParser

    parser = OptionParser(version='%prog 0.1', usage='%prog [OPTIONS] IMAGES')
    parser.add_option('-s', '--size', action='store', type=str,
            default='640x480', help='Resize to this size (default=%default)')
    parser.add_option('-d', '--target-directory', action='store', type=str,
            default='Thumbs', help='Target directory (default=%default)')
    parser.add_option('-t', '--test', action='store_true', default=False,
            help="test only: doesn't actually rename anything")
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help='show on STDOUT what happens')
    return parser

def resize(options, image):
    size = map(int, options.size.split('x'))
    dest = join(options.target_directory, basename(image))
    if options.verbose:
        print('Resizing %s @ %dx%d as %s' % (image, size[0], size[1], dest))
    im = Image.open(image)
    im.thumbnail(size, Image.ANTIALIAS)
    if not options.test:
        im.save(dest)

def main():
    parser = parse_options()
    options, args = parser.parse_args()
    if not args:
        raise SystemExit(parser.print_usage())
    try:
        mkdir(options.target_directory)
    except OSError:
        pass
    for image in args:
        resize(options, image)

if __name__ == '__main__':
    main()
