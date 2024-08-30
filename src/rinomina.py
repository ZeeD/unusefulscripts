from logging import INFO
from logging import basicConfig
from logging import getLogger
from optparse import Option
from optparse import OptionParser
from optparse import OptionValueError
from optparse import Values
from pathlib import Path

from PIL.Image import open

logger = getLogger(__name__)


def check_dir(
    _option: Option, _opt: str, value: str, parser: OptionParser
) -> None:
    """Check if a value is a directory."""
    if not Path(value).is_dir():
        raise OptionValueError(value)
    if parser.values is None:  # noqa: PD011
        parser.values = Values()
    parser.values.dir = value  # noqa: PD011


def sort_images(image_file_name: Path) -> tuple[float, float]:
    """Regole.

    - una immagine è più grande di un'altra se la sua superficie è maggiore.
        --> x*y deve essere grande
    - a parità di superficie, si ritiene maggiore quella più quadrata
        --> x == y --> abs(x-y) deve -> 0 positivamente
        --> -abs(x-y) deve -> 0 negativame (e più grande è meglio è)
    - a parità di diagonale, sono uguali :P
    """
    try:
        im_x, im_y = open(image_file_name).size
    except Exception:
        logger.exception(image_file_name)
        raise
    else:
        return (im_x * im_y, -abs(im_x - im_y))


def mkparser() -> OptionParser:
    """Create and return an OptionParser instance with all options added."""
    ret = OptionParser(
        version='%prog 0.3',
        usage="""%prog [OPTS] [SCRAP|...]
            Rename files with a leading number, except those SCRAP-ped""",
    )
    ret.add_option(
        '-d',
        '--dir',
        action='callback',
        type='string',
        default='.',
        callback=check_dir,
        help="Sort files in DIR (default='%default')",
    )
    ret.add_option(
        '-b',
        '--begin',
        type='int',
        default=1,
        metavar='N',
        help='Start enumerating from N (default=%default)',
    )
    ret.add_option(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Show on STDOUT what happens',
    )
    ret.add_option(
        '-c',
        '--cifre',
        type='int',
        default=0,
        metavar='N',
        help='Use at least N chars to represents the numbers',
    )
    ret.add_option(
        '-u',
        '--use-dirname',
        action='store_true',
        default=False,
        help='Use the dir name instead of the original name file',
    )
    ret.add_option(
        '-i',
        '--imgs',
        action='store_true',
        default=False,
        help='Files are images: sort then by pixel resolution, not by name',
    )
    ret.add_option(
        '-t',
        '--test',
        action='store_true',
        default=False,
        help="Test only: doesn't actually rename anything",
    )
    ret.add_option(
        '-a',
        '--also-dir',
        action='store_true',
        default=False,
        help='Rename also the directories (not recursive!)',
    )
    return ret


def parse_and_validate_args() -> tuple[Values, set[int]]:
    """Wrap mkparser()."""
    parser = mkparser()
    options, args = parser.parse_args()
    scarti = {int(parametro) for parametro in args}
    return options, scarti


def mk_associations(
    filenames: list[Path], begin: int, scarti: set[int]
) -> tuple[dict[Path, int], int]:
    """Return a 2-tuple: (dict(source_name: number), max_used_number_length)."""
    associations = {}
    number = begin
    for filename in filenames:
        while number in scarti:
            number += 1
        associations[filename] = number
        number += 1
    return associations, len(str(number - 1))


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    options, scarti = parse_and_validate_args()
    curdir = Path(options.dir)
    filenames = sorted(
        (
            filename
            for filename in curdir.iterdir()
            if filename.is_file() or options.also_dir and filename.is_dir()
        ),
        key=sort_images if options.imgs else None,
        reverse=options.imgs,
    )

    associa, max_length = mk_associations(filenames, options.begin, scarti)

    if options.use_dirname:
        nome_directory = curdir.resolve().name

    fmt = ' - %%.%dd' if options.use_dirname else '%%.%dd - '
    formato = fmt % max(options.cifre, max_length)

    for sorgente, intero in sorted(associa.items()):
        destinazione = sorgente.with_name(
            (nome_directory + formato % intero + sorgente.suffix)
            if options.use_dirname
            else (formato % intero + sorgente.name)
        )
        if destinazione.exists():
            logger.warning('%r è già usato!', destinazione)
            continue

        if options.verbose:
            if options.imgs:
                im_x, im_y = open(sorgente).size
                logger.info(
                    '%s -> %s (%sx%s, %s, %s)',
                    sorgente,
                    destinazione,
                    im_x,
                    im_y,
                    im_x * im_y,
                    -abs(im_x - im_y),
                )
            else:
                logger.info('%s -> %s', sorgente, destinazione)
        if not options.test:
            sorgente.rename(destinazione)


if __name__ == '__main__':
    main()
