from collections.abc import Hashable
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from itertools import groupby
from itertools import tee
from itertools import zip_longest
from logging import INFO
from logging import basicConfig
from logging import getLogger
from optparse import OptionGroup
from optparse import OptionParser
from optparse import Values
from os.path import join
from os.path import split
from os.path import splitext
from pathlib import Path
from re import search
from subprocess import PIPE
from subprocess import Popen
from typing import TYPE_CHECKING
from typing import Any
from typing import Final
from typing import TypeVar

from PIL import ExifTags
from PIL import Image

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from collections.abc import Iterator

logger = getLogger(__name__)


class MetaData:
    supported_tags: Final = {
        'DateTime': 306,
        'DateTimeOriginal': 36867,
        'DateTimeDigitized': 36868,
    }

    filename: Path
    datetime: datetime

    def __init__(self, image_filename: str, tagname: str) -> None:
        """Construct a datetime object.

        Use the exif information stored into the image named image_filename
        """
        self.filename = Path(image_filename)
        tag = MetaData.supported_tags[tagname]
        if ExifTags.TAGS[tag] != tagname:
            raise ValueError(tag)
        exiftags = Image.open(image_filename).getexif()
        if not exiftags:
            msg = f'{image_filename}: No exif tags found'
            raise RuntimeError(msg)
        self.datetime = datetime.strptime(
            exiftags[tag], '%Y:%m:%d %H:%M:%S'
        ).astimezone(UTC)
        dirname, basename = split(image_filename)
        basename, ext = splitext(basename)
        self.split = dirname, basename, ext


class MovMetaData(MetaData):
    """Support for exif tags in .mov files."""

    def __init__(
        self, mov_filename: str, _tagname: str | None
    ) -> None:  # tagname is ignored.
        self.filename = Path(mov_filename)
        try:
            cmdline = ('exiftool', '-CreateDate', '-b', mov_filename)
            stdout = Popen(cmdline, stdout=PIPE, text=True).communicate()[0]
        except OSError:
            msg = f'{mov_filename}: No exif tags found (maybe no exiftool?)'
            raise RuntimeError(msg) from None
        else:
            self.datetime = datetime.strptime(
                stdout, '%Y:%m:%d %H:%M:%S'
            ).astimezone(UTC)
            dirname, basename = split(mov_filename)
            basename, ext = splitext(basename)
            self.split = dirname, basename, ext


class AviMetaData(MetaData):
    """Support for exif tags in .avi files."""

    def __init__(
        self, mov_filename: str, _tagname: str | None
    ) -> None:  # tagname is ignored.
        self.filename = Path(mov_filename)
        cmdline = ('exiftool', '-DateTimeOriginal', '-b', mov_filename)
        stdout = Popen(cmdline, stdout=PIPE, text=True).communicate()[0]
        self.datetime = datetime.strptime(
            stdout, '%Y:%m:%d %H:%M:%S'
        ).astimezone(UTC)
        dirname, basename = split(mov_filename)
        basename, ext = splitext(basename)
        self.split = dirname, basename, ext


def heuristic_by_date(pair: tuple[MetaData, MetaData | None]) -> Hashable:
    """Group by date."""
    (a, _) = pair
    return a.datetime.date()


class HeuristicByHourDistance:
    """Group if a was made at most max_hour_interval before b."""

    def __init__(self, max_hour_interval: int = 12) -> None:
        self.timedelta = timedelta(hours=max_hour_interval)
        self.returnValue = True

    def __call__(self, pair: tuple[MetaData, MetaData | None]) -> bool:
        (a, b) = pair
        if b is None or (b.datetime - a.datetime) < self.timedelta:
            return self.returnValue

        self.returnValue = not self.returnValue
        return not self.returnValue


def heuristic_all_together(_pair: tuple[MetaData, MetaData | None]) -> bool:
    """'Stupid' heuristic: all images belong to the same group."""
    return True


T = TypeVar('T')


def group_by(
    iterable: 'Iterable[T]', grouper: 'Callable[[tuple[T, T | None]], Any]'
) -> 'Iterable[Iterable[T]]':
    """*Wrong* wrapper around itertools.groupby."""
    a, b = tee(iterable)
    next(b)
    return ((g[0] for g in e[1]) for e in groupby(zip_longest(a, b), grouper))


def get_common_prefix(list_of_datetimes: 'Iterator[datetime]') -> str:
    """Extract a common_prefix, the kind of YYYY-MM-DD+(DD+1)+...

    NOTE: it doesn't support sequences between 2 different months!
    """
    date = next(list_of_datetimes)  # cry if list_of_datetimes is empty
    ret = [date.strftime('%F')]
    for next_date in list_of_datetimes:
        if next_date.day > date.day + 1:
            raise ValueError(next_date.day)
        if next_date.year != date.year:
            ret.append(next_date.strftime('+%Y-%m-%d'))
        elif next_date.month != date.month:
            ret.append(next_date.strftime('+%m-%d'))
        elif next_date.day != date.day:
            ret.append(next_date.strftime('+%d'))
        date = next_date
    return ''.join(ret)


def new_file(metadata: MetaData, common_prefix: str, options: Values) -> str:
    dirname, basename, ext = metadata.split
    # FIX: se common_prefix è della forma DD+(DD), vorrò avere come nome file
    # "DD hh_mm_ss.jpg", e non solo 'hh_mm_ss.jpg'
    if search(r'\+\d{2}$', common_prefix):
        filename = metadata.datetime.strftime('%d %T')
    else:
        filename = metadata.datetime.strftime('%T')

    if options.group_in_directories:
        central_part = join(common_prefix, filename)
    else:
        central_part = common_prefix + ' ' + filename
    if options.preserve_filename:
        central_part += ' - ' + basename
    return join(dirname, central_part) + ext


def new_dir(metadata: MetaData, common_prefix: str, _options: Values) -> Path:
    return metadata.filename.parent / common_prefix


def get_heuristic(
    options: Values,
) -> 'Callable[[tuple[MetaData, MetaData | None]], Any]':
    if options.heuristic:
        return HeuristicByHourDistance()
    if options.all_togheter:
        return heuristic_all_together
    return heuristic_by_date


def get_metadatas(options: Values, args: list[str]) -> list[MetaData]:
    metadatas = []
    for arg in args:
        md: MetaData
        if arg.endswith('.mov'):
            md = MovMetaData(arg, None)
        elif arg.endswith('.avi'):
            md = AviMetaData(arg, None)
        else:
            md = MetaData(arg, options.key)
        metadatas.append(md)

    if not metadatas:
        logger.error('No valid files!')
        raise SystemExit

    return metadatas


def estrai_data(options: Values, args: list[str]) -> None:
    metadatas = get_metadatas(options, args)

    if options.extract_only:
        for metadata in metadatas:
            logger.info('%s:\t%s', metadata.filename, metadata.datetime)
        return

    heuristic = get_heuristic(options)
    for mdos in group_by(
        sorted(metadatas, key=lambda i: i.datetime), heuristic
    ):
        mdos1, mdos2 = tee(mdos)
        common_prefix = get_common_prefix(md.datetime for md in mdos1)
        for metadata in mdos2:
            if options.group_in_directories:
                dirname = new_dir(metadata, common_prefix, options)
                if not dirname.is_dir():
                    if options.verbose:
                        logger.info('mkdir %r', dirname)
                    if not options.test:
                        dirname.mkdir(parents=True)
            filename = new_file(metadata, common_prefix, options)
            if options.verbose:
                logger.info('mv %r %r', metadata.filename, filename)
            if not options.test:
                metadata.filename.rename(filename)


def parse_args() -> tuple[Values, list[str]]:
    """Create an OptionParser istance, add the user options and return it."""
    parser = OptionParser(version='%prog 0.1', usage='%prog [OPTIONS] PHOTOS')
    parser.add_option(
        '-d',
        '--group-in-directories',
        action='store_true',
        default=False,
        help='group images in directories, once per day',
    )
    group = OptionGroup(parser, 'Heuristic strategies')
    group.add_option(
        '-g',
        '--heuristic',
        action='store_true',
        default=False,
        help='use heuristic to group images spanned in various days',
    )
    group.add_option(
        '-a',
        '--all-togheter',
        action='store_true',
        default=False,
        help='group all images',
    )
    group.add_option(
        '-b',
        '--by-date',
        action='store_true',
        default=False,
        help='group using the date (default)',
    )
    parser.add_option_group(group)
    parser.add_option(
        '-p',
        '--preserve-filename',
        action='store_true',
        default=False,
        help='preserve original filename',
    )
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

    fmt = 'use KEY to extract date from the image (default=%s, available=%s)'
    parser.add_option(
        '-k',
        '--key',
        action='store',
        default='DateTime',
        type=str,
        help=fmt % ('%default', MetaData.supported_tags.keys()),
    )
    parser.add_option(
        '-x',
        '--extract-only',
        action='store_true',
        default=False,
        help='just show the exif date of the images',
    )

    options, args = parser.parse_args()
    if (
        (options.heuristic and options.all_togheter)
        or (options.heuristic and options.by_date)
        or (options.all_togheter and options.by_date)
    ):
        parser.error('Heuristic options are mutually exclusive')

    if not args:
        parser.print_usage()
        raise SystemExit

    return options, args


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    options, args = parse_args()
    estrai_data(options, args)


if __name__ == '__main__':
    main()
