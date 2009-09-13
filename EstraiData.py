#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from os.path import split, splitext, join, isdir
import ExifTags
import Image
from itertools import groupby, tee, izip_longest
from optparse import OptionParser
from os import mkdir, rename

class MetaData(object):
    _supported_tags = { 'DateTime': 306, 'DateTimeOriginal': 36867,
            'DateTimeDigitized': 36868 }
    def __init__(self, image_filename, tagname='DateTime'):
        """construct a datetime object from the exif information stored into the
        image which is named image_filename"""
        self.filename = image_filename
        tag = MetaData._supported_tags[tagname]
        assert ExifTags.TAGS[tag] == tagname # maybe it's changed...
        exiftags = Image.open(image_filename)._getexif()
        if not exiftags:
            raise StandardError("%s: No exif tags found" % image_filename)
        self.datetime = datetime.strptime(exiftags[tag], '%Y:%m:%d %H:%M:%S')
        dirname, basename = split(self.filename)
        basename, ext = splitext(basename)
        self.split = dirname, basename, ext

def heuristic_by_date((a, b)):
    """Default heuristic, group by date"""
    return a.datetime.date()

class make_heuristic_by_hour_distance(object):
    """Cool heuristic: group if a was made at most max_hour_interval before b"""
    def __init__(self, max_hour_interval=12):
        self.timedelta = timedelta(hours=max_hour_interval)
        self.returnValue = True

    def __call__(self, (a, b)):
        if b is None or (b.datetime-a.datetime) < self.timedelta:
            return self.returnValue
        else:
            self.returnValue = not self.returnValue
            return not self.returnValue

def group_by(iterable, grouper):
    """*wrong* wrapper around itertools.groupby"""
    a, b = tee(iterable)
    next(b)
    return ((g[0] for g in e[1]) for e in groupby(izip_longest(a, b), grouper))

def get_common_prefix(list_of_datetimes):
    """Extract a common_prefix, the kind of YYYY-MM-DD+(DD+1)+...
    *YEAH*, it doesn't support sequences between 2 different months, so what?"""
    date = list_of_datetimes.next() # cry if list_of_datetimes is empty
    ret = [ date.strftime('%F') ]
    for next_date in list_of_datetimes:
        assert next_date.day <= date.day + 1
        if next_date.day != date.day:
            ret.append(next_date.strftime('+%d'))
            date = next_date
    return ''.join(ret)

def new_file(metadata_object, common_prefix, options):
    from re import search
    dirname, basename, ext = metadata_object.split
    # FIX: se common_prefix è della forma DD+(DD), vorrò avere come nome file
    # "DD hh_mm_ss.jpg", e non solo 'hh_mm_ss.jpg'
    if search('\+\d{2}$', common_prefix):
        filename = metadata_object.datetime.strftime('%d %T')
    else:
        filename = metadata_object.datetime.strftime('%T')

    if options.group_in_directories:
        central_part = join(common_prefix, filename)
    else:
        central_part = common_prefix + ' ' + filename
    if options.preserve_filename:
        central_part += ' - ' + basename
    return join(dirname, central_part) + ext

def new_dir(metadata_object, common_prefix, options):
    dirname, basename, ext = metadata_object.split
    return join(dirname, common_prefix)

def main(options, args):
    if options.heuristic:
        heuristic = make_heuristic_by_hour_distance()
    else:
        heuristic = heuristic_by_date
    # mdos -> MetaData ObjectS
    mdoss = []
    for arg in args:
        try:
            mdoss.append(MetaData(arg))
        except Exception as e:
            print "%s: %s" % (arg, e)
    for mdos in group_by(sorted(mdoss, key=lambda i: i.datetime), heuristic):
        mdos1, mdos2 = tee(mdos)
        common_prefix = get_common_prefix(mdo.datetime for mdo in mdos1)
        for mdo in mdos2:
            if options.group_in_directories:
                dirname = new_dir(mdo, common_prefix, options)
                if not isdir(dirname):
                    if options.verbose:
                        print 'mkdir %r' % dirname
                    if not options.test:
                        mkdir(dirname)
            filename = new_file(mdo, common_prefix, options)
            if options.verbose:
                print 'mv %r %r' % (mdo.filename, filename)
            if not options.test:
                rename(mdo.filename, filename)

def parse_options():
    """Create an OptionParser istance, add the user options and return it"""
    parser = OptionParser(version='%prog 0.1', usage='%prog [OPTIONS] PHOTOS')
    parser.add_option('-d', '--group-in-directories', action='store_true',
            default=False, help='group images in directories, once per day')
    parser.add_option('-g', '--heuristic', action='store_true', default=False,
            help='use heuristic to _g_roup images spanned in various days')
    parser.add_option('-p', '--preserve-filename', action='store_true',
            default=False, help='preserve original filename')
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
