from logging import INFO
from logging import basicConfig
from logging import getLogger
from optparse import OptionParser
from optparse import Values
from pathlib import Path

from PIL import Image

logger = getLogger(__name__)


def parse_options() -> OptionParser:
    """Create an OptionParser istance, add the user options and return it."""
    parser = OptionParser(version='%prog 0.1', usage='%prog [OPTIONS] IMAGES')
    parser.add_option(
        '-s',
        '--size',
        action='store',
        type=str,
        default='640x480',
        help='Resize to this size (default=%default)',
    )
    parser.add_option(
        '-d',
        '--target-directory',
        action='store',
        type=str,
        default='Thumbs',
        help='Target directory (default=%default)',
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
    return parser


def resize(options: Values, image: str) -> None:
    _size_0_raw, _size_1_raw = options.size.split('x')
    size = float(_size_0_raw), float(_size_1_raw)
    dest = Path(options.target_directory) / Path(image).name
    if options.verbose:
        logger.info('Resizing %s @ %dx%d as %s', image, size[0], size[1], dest)
    im = Image.open(image)
    im.thumbnail(size, Image.Resampling.LANCZOS)
    if not options.test:
        im.save(dest)


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    parser = parse_options()
    options, args = parser.parse_args()
    if not args:
        parser.print_usage()
        raise SystemExit
    Path(options.target_directory).mkdir(parents=True, exist_ok=True)
    for image in args:
        resize(options, image)


if __name__ == '__main__':
    main()
