from logging import INFO
from logging import basicConfig
from logging import getLogger
from optparse import OptionParser
from optparse import Values
from os import walk
from pathlib import Path
from typing import TYPE_CHECKING
from typing import override

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = getLogger(__name__)


def filenames(args: list[str], /, *, recursive: bool) -> 'Iterable[Path]':
    for arg in args:
        if recursive:
            for base, dirs, files in walk(arg, topdown=False):
                for file_ in files:
                    yield Path(base) / file_
                for dir_ in dirs:
                    yield Path(base) / dir_
        yield Path(arg)


def sistema_case_single(options: Values, path_orig: Path) -> None:
    chunks_orig = path_orig.name.split(' - ')

    chunks_new: list[str]
    if options.document:
        # il primo elemento contiene nomi propri, quindi capitalizzo tutto
        chunks_new = [', '.join(a.capitalize() for a in chunks_orig[0].split())]
        chunks_new.extend([el.capitalize() for el in chunks_orig[1:]])
    else:
        chunks_new = [el.capitalize() for el in chunks_orig]
    name_new = ' - '.join(chunks_new)

    # per le S.I.G.L.E.
    chunks_new = name_new.split('.')
    for i, chunk in enumerate(chunks_new):
        if not chunk[-2:-1].isalnum():
            try:
                chunks_new[i] = chunk[:-1] + chunk[-1].upper()
            except IndexError:
                chunks_new[i] = chunk[:-1]  # per "..."
    name_new = '.'.join(chunks_new)

    path_new = path_orig.with_name(name_new)
    if path_new.exists():
        logger.warning('%s è già usato!', path_new)
        return

    if options.verbose:
        logger.info('%s -> %s', path_orig, path_new)
    if not options.test:
        path_orig.rename(path_new)


def sistema_case(options: Values, paths: 'Iterable[Path]') -> None:
    for path in paths:
        sistema_case_single(options, path)


class MyOptionParser(OptionParser):
    @override
    def check_values(
        self, values: Values, args: list[str]
    ) -> tuple[Values, list[str]]:
        if not args:
            self.error('Must set at least a file')
        for arg in args:
            if not Path(arg).exists():
                self.error(f'File not found: {arg!r}')
        return super().check_values(values, args)


def parse_args() -> tuple[Values, list[str]]:
    parser = MyOptionParser(version='%prog 0.7', usage='%prog FILE...')
    parser.add_option(
        '-d',
        '--document',
        action='store_true',
        help='Modalità per documenti (Nome Cognome - Documento.ext)',
    )
    parser.add_option(
        '-v',
        '--verbose',
        action='store_true',
        help='Mostra su STDOUT le azioni compiute',
    )
    parser.add_option(
        '-t',
        '--test',
        action='store_true',
        help="Non compiere nessuna rinomina (utile con '--verbose')",
    )
    parser.add_option(
        '-r',
        '-R',
        '--recursive',
        action='store_true',
        help='Agisci in modo ricorsivo anche nelle sotto-directory',
    )
    return parser.parse_args()


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    options, args = parse_args()
    sistema_case(options, filenames(args, recursive=options.recursive))


if __name__ == '__main__':
    main()
