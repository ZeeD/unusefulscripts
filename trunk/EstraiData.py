#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from os.path import split, splitext, join, isdir
import ExifTags
import Image
from itertools import groupby, tee, izip_longest
from optparse import OptionParser, OptionGroup, SUPPRESS_HELP
from os import mkdir, rename
from subprocess import Popen, PIPE


class MetaData(object):
    _supported_tags = {
        'DateTime': 306,
        'DateTimeOriginal': 36867,
        'DateTimeDigitized': 36868
    }

    def __init__(self, image_filename, tagname):
        """construct a datetime object from the exif information stored into
        the image which is named image_filename"""
        self.filename = image_filename
        tag = MetaData._supported_tags[tagname]
        assert ExifTags.TAGS[tag] == tagname    # maybe it's changed...
        exiftags = Image.open(image_filename)._getexif()
        if not exiftags:
            raise Exception('%s: No exif tags found' % self.filename)
        self.datetime = datetime.strptime(exiftags[tag], '%Y:%m:%d %H:%M:%S')
        dirname, basename = split(self.filename)
        basename, ext = splitext(basename)
        self.split = dirname, basename, ext


class MovMetaData(MetaData):
    """Support for exif tags in .mov files"""
    def __init__(self, mov_filename, tagname):  # tagname is ignored.
        self.filename = mov_filename
        try:
            cmdline = ('exiftool', '-CreateDate', '-b', self.filename)
            stdout = Popen(cmdline, stdout=PIPE).communicate()[0]
        except OSError as e:
            msg_fmt = '%s: No exif tags found (maybe no exiftool installed?)'
            raise Exception(msg_fmt % self.filename)
        else:
            self.datetime = datetime.strptime(stdout, '%Y:%m:%d %H:%M:%S')
            dirname, basename = split(self.filename)
            basename, ext = splitext(basename)
            self.split = dirname, basename, ext


class AviMetaData(MetaData):
    """Support for exif tags in .avi files"""
    def __init__(self, mov_filename, tagname):  # tagname is ignored.
        self.filename = mov_filename
        cmdline = ('exiftool', '-DateTimeOriginal', '-b', self.filename)
        stdout = Popen(cmdline, stdout=PIPE).communicate()[0]
        self.datetime = datetime.strptime(stdout, '%Y:%m:%d %H:%M:%S')
        dirname, basename = split(self.filename)
        basename, ext = splitext(basename)
        self.split = dirname, basename, ext


def heuristic_by_date((a, b)):
    """Default heuristic, group by date"""
    return a.datetime.date()


class make_heuristic_by_hour_distance(object):
    "Cool heuristic: group if a was made at most max_hour_interval before b"
    def __init__(self, max_hour_interval=12):
        self.timedelta = timedelta(hours=max_hour_interval)
        self.returnValue = True

    def __call__(self, (a, b)):
        if b is None or (b.datetime-a.datetime) < self.timedelta:
            return self.returnValue
        else:
            self.returnValue = not self.returnValue
            return not self.returnValue


def heuristic_all_together((a, b)):
    """'Stupid' heuristic: all images belong to the same group"""
    return True


def group_by(iterable, grouper):
    """*wrong* wrapper around itertools.groupby"""
    a, b = tee(iterable)
    next(b)
    return ((g[0] for g in e[1]) for e in groupby(izip_longest(a, b), grouper))


def get_common_prefix(list_of_datetimes):
    """Extract a common_prefix, the kind of YYYY-MM-DD+(DD+1)+...
    NOTE: it doesn't support sequences between 2 different months!"""
    date = next(list_of_datetimes)  # cry if list_of_datetimes is empty
    ret = [date.strftime('%F')]
    for next_date in list_of_datetimes:
        assert next_date.day <= date.day + 1
        if next_date.year != date.year:
            ret.append(next_date.strftime('+%Y-%m-%d'))
        elif next_date.month != date.month:
            ret.append(next_date.strftime('+%m-%d'))
        elif next_date.day != date.day:
            ret.append(next_date.strftime('+%d'))
        date = next_date
    return ''.join(ret)


def test_get_common_prefix():
    f = get_common_prefix
    i_es = (
        (
            iter([
                datetime(2009, 11, 29),
                datetime(2009, 11, 30)]),
            '2009-11-29+30'),
        (
            iter([
                datetime(2009, 11, 29),
                datetime(2009, 11, 29),
                datetime(2009, 11, 30),
                datetime(2009, 12, 1),
                datetime(2009, 12, 2)]),
            '2009-11-29+30+12-01+02'),
        (
            iter([
                datetime(2009, 12, 31),
                datetime(2010, 1, 1)]),
            '2009-12-31+2010-01-01')
    )
    for i, e in i_es:
        o = f(i)
        assert o == e, "%s(%s) == %s != %s" % (f.__name__, i, o, e)


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
    elif options.all_togheter:
        heuristic = heuristic_all_together
    else:
        heuristic = heuristic_by_date
    # mdos -> MetaData ObjectS
    mdoss = []
    for arg in args:
        try:
            if arg.endswith('.mov'):
                mdo = MovMetaData(arg, None)
            elif arg.endswith('.avi'):
                mdo = AviMetaData(arg, None)
            else:
                mdo = MetaData(arg, options.key)
            mdoss.append(mdo)
        except Exception as e:
            print("%s: %s %s" % (arg, e, type(e)))
    if options.extract_only:
        for mdo in mdoss:
            print("%s:\t%s" % (mdo.filename, mdo.datetime))
        return
    if not mdoss:
        raise SystemExit('No valid files!')
    if options.test:
        fake_dirs = set()
    for mdos in group_by(sorted(mdoss, key=lambda i: i.datetime), heuristic):
        mdos1, mdos2 = tee(mdos)
        common_prefix = get_common_prefix(mdo.datetime for mdo in mdos1)
        for mdo in mdos2:
            if options.group_in_directories:
                dirname = new_dir(mdo, common_prefix, options)
                if ((not options.test and not isdir(dirname)) or
                        (options.test and dirname not in fake_dirs)):
                    if options.verbose:
                        print('mkdir %r' % dirname)
                    if options.test:
                        fake_dirs.add(dirname)
                    else:
                        mkdir(dirname)
            filename = new_file(mdo, common_prefix, options)
            if options.verbose:
                print('mv %r %r' % (mdo.filename, filename))
            if not options.test:
                rename(mdo.filename, filename)


def parse_options():
    """Create an OptionParser istance, add the user options and return it"""
    parser = OptionParser(version='%prog 0.1', usage='%prog [OPTIONS] PHOTOS')
    parser.add_option(
        '-d', '--group-in-directories',
        action='store_true', default=False,
        help='group images in directories, once per day')
    group = OptionGroup(parser, 'Heuristic strategies')
    group.add_option(
        '-g', '--heuristic',
        action='store_true', default=False,
        help='use heuristic to group images spanned in various days')
    group.add_option(
        '-a', '--all-togheter',
        action='store_true', default=False,
        help='group all images')
    group.add_option(
        '-b', '--by-date',
        action='store_true', default=False,
        help='group using the date (default)')
    parser.add_option_group(group)
    parser.add_option(
        '-p', '--preserve-filename',
        action='store_true', default=False,
        help='preserve original filename')
    parser.add_option(
        '-t', '--test',
        action='store_true', default=False,
        help="test only: doesn't actually rename anything")
    parser.add_option(
        '-v', '--verbose',
        action='store_true', default=False,
        help='show on STDOUT what happens')

    fmt = 'use KEY to extract date from the image (default=%s, available=%s)'
    parser.add_option(
        '-k', '--key',
        action='store', default='DateTime', type=str,
        help=fmt % ('%default', MetaData._supported_tags.keys()))
    parser.add_option(
        '--unit-test',
        action='store_true',
        help=SUPPRESS_HELP)
    parser.add_option(
        '-x', '--extract-only',
        action='store_true', default=False,
        help="just show the exif date of the images")
    return parser


def do_tests():
    try:
        test_get_common_prefix()
    except AssertionError as e:
        print(e)
    else:
        print('No errors!')

if __name__ == '__main__':
    parser = parse_options()
    options, args = parser.parse_args()

    if ((options.heuristic and options.all_togheter) or
            (options.heuristic and options.by_date) or
            (options.all_togheter and options.by_date)):
        parser.error('Heuristic options are mutually exclusive')

    if options.unit_test:
        raise SystemExit(do_tests())
    if not args:
        raise SystemExit(parser.print_usage())
    main(options, args)
