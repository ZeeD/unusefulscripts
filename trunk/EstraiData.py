#!/usr/bin/env python

def parse_exif_date(string):
    """Take a string in the format YYYY:MM:DD HH:MM:SS
    return a datetime.datetime object"""
    from datetime import datetime
    YYYY_MM_DD, hh_mm_ss = string.split(' ')
    (YYYY, MM, DD), (hh, mm, ss) = YYYY_MM_DD.split(':'), hh_mm_ss.split(':')
    YYYY, MM, DD, hh, mm, ss = map(int, (YYYY, MM, DD, hh, mm, ss))
    return datetime(year=YYYY, month=MM, day=DD, hour=hh, minute=mm, second=ss)

def extract_date(image_filename, tagname='DateTime'):
    """return a datetime object from the exif information stored into the image
    which is named image_filename"""
    supported_tags = { 'DateTime': 306, 'DateTimeOriginal': 36867,
            'DateTimeDigitized': 36868 }
    tag = supported_tags[tagname] # raise exception if not supported
    import ExifTags
    assert ExifTags.TAGS[tag] == tagname # maybe it's changed...
    import Image
    return parse_exif_date(Image.open(image_filename)._getexif()[tag])

def do_rename(mapping):
    """take a dict of the type { datetime, path },
    rename the file in the path accornding to datetime"""
    for date in sorted(mapping):
        print "Now I'm gonna mv `%s` to `%s'" % (mapping[date], date)

def main(options, args):
    mapping = {}
    for param in args:
        mapping[extract_date(param)] = param
    do_rename(mapping)

def parse_options():
    """Parse user options
    return options, args (== OptionParser(...).parse_args())
    """
    from optparse import OptionParser
    parser = OptionParser(version='%prog 0.1', usage='%prog [OPTIONS] PHOTOS')
    parser.add_option('-d', '--group-in-directories', action='store_true',
            default=False, help='group images in directories, once per day')
    parser.add_option('-g', '--heuristic', action='store_true', default=False,
            help='use heuristic to _g_roup images spanned in various days')
    parser.add_option('-p', '--preserve-filename', action='store_true',
            default=False, help='preserve original filename')
    #parser.add_option('-r', '--recursive', action='store_true', default=False,
            #help='Apply recursively also to directories') # doesn't makes sense
    parser.add_option('-t', '--test', action='store_true', default=False,
            help="test only: doesn't actually rename anything")
    parser.add_option('-v', '--verbose', action='store_true', default=False,
            help='show on STDOUT what happens')
    return parser

if __name__ == '__main__':
    parser = parse_options()
    options, args = parser.parse_args()
    if not args:
        raise SystemExit(parser.print_usage())
    main(options, args)
