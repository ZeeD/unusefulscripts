from logging import INFO
from logging import basicConfig
from logging import getLogger
from optparse import OptionParser
from optparse import Values
from pathlib import Path

logger = getLogger(__name__)


def build_option_parser() -> OptionParser:
    """Create an OptionParser istance, add the user options and return it."""
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


def ripristina(output: str, options: Values) -> None:
    for row in output.split('\n'):
        old_name, new_name = row.split(options.separator)
        if options.verbose:
            logger.info('mv %r %r;', new_name, old_name)
        if not options.test:
            Path(new_name).rename(old_name)


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    option_parser = build_option_parser()
    options, args = option_parser.parse_args()
    output = args[0]

    ripristina(output, options)


if __name__ == '__main__':
    main()
