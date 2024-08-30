from logging import INFO
from logging import basicConfig
from logging import getLogger
from optparse import OptionParser
from optparse import Values
from pathlib import Path

logger = getLogger(__name__)


def parse_args() -> tuple[Values, list[str]]:
    parser = OptionParser(
        version='%prog 0.2.0',
        usage="""%prog (FILE|'')...
        Mette un numero in ordine crescente davanti ad ogni FILE specificato
        Usa '' per inserire 'buchi\'""",
    )
    parser.add_option(
        '-b',
        '--begin',
        type='int',
        default=1,
        metavar='N',
        help='Inizia a numerare da N (default = %default)',
    )
    parser.add_option(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Mostra sullo STDOUT cosa accade',
    )
    parser.add_option(
        '-c',
        '--cifre',
        type='int',
        default=0,
        metavar='N',
        help='Usa almeno N cifre per i numeri (default = %default)',
    )
    parser.add_option(
        '-t',
        '--test',
        action='store_true',
        default=False,
        help='Non effettuare davvero la rinomina dei file (utile con -v)',
    )
    parser.add_option(
        '-u',
        '--use-dirname',
        action='store_true',
        default=False,
        help='Invece del nome originale, usa il nome della directory',
    )
    parser.add_option(
        '-p',
        '--pre',
        type=str,
        default='',
        metavar='STR',
        help='Inserisci la stringa STR in testa',
    )
    parser.add_option(
        '-s',
        '--switch',
        action='store_true',
        default=False,
        help='Inverti di posizione nome del file e numero (utile con -u)',
    )

    return parser.parse_args()


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    options, args = parse_args()
    i = 0
    substitutions: list[tuple[Path, int]] = []
    for i, param in enumerate(args, start=options.begin):
        if param:
            substitutions.append((Path(param).resolve(), i))

    fmt = f'%.{max(options.cifre, len(str(i)))}d'

    for source, i in substitutions:
        prefix = fmt % i
        fn = source.parent.name if options.use_dirname else source.stem
        file_name = f'{fn} - {prefix}' if options.switch else f'{prefix} - {fn}'
        dest = source.with_name(f'{options.pre}{file_name}{source.suffix}')
        if dest.exists():
            logger.error('%r è già usato!', dest)
            raise RuntimeWarning
        if options.verbose:
            logger.info('%s -> %s', source, dest)
        if not options.test:
            source.rename(dest)


if __name__ == '__main__':
    main()
