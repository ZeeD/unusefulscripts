from itertools import groupby
from itertools import starmap
from logging import INFO
from logging import basicConfig
from logging import getLogger
from math import log10
from optparse import OptionParser
from optparse import Values
from os.path import join
from os.path import split
from pathlib import Path
from shutil import move as shmove
from typing import TYPE_CHECKING
from typing import cast

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from collections.abc import Sequence

logger = getLogger(__name__)


def warn(message: str, *, error: bool = False) -> None:
    if error:
        logger.error(message)
        raise SystemError
    logger.warning(message)


def exists_warn(path: Path) -> bool:
    return_value = path.exists()
    if not return_value:
        warn(f'{path!r} does not exist!')
    return return_value


def find_integers(string: str) -> tuple[str | int, ...]:
    """Split a string in alternating strings and integers.

    The first element will always be a string.
    """
    out: list[str | int] = []
    begin = end = 0
    string_len = len(string)
    while end < string_len:
        if string[end].isdigit():
            out.append(string[begin:end])
            begin = end
            while end < string_len and string[end].isdigit():
                end += 1
            out.append(int(string[begin:end]))
            begin = end
        end += 1
    out.append(string[begin:end])
    return tuple(out)


def find_integers2(s: str) -> tuple[str | int, ...]:
    return (('',) if not s or s[0].isdigit() else ()) + tuple(
        int(''.join(b)) if a else ''.join(b) for a, b in groupby(s, str.isdigit)
    )


def find_integers3(string: str) -> tuple[str | int, ...]:
    if not string:
        return ('',)
    ret: list[str | int] = []
    if string[0].isdigit():
        ret.append('')
    for is_digit, it in groupby(string, str.isdigit):
        value: str | int = ''.join(it)
        if is_digit:
            value = int(value)
        ret.append(value)
    return tuple(ret)


def multi_max(matrix: 'Iterable[tuple[int | str, ...]]') -> list[int]:
    """Get max values for each odd column.

    matrix = (
        (Stringa, Numero, Stringa, Numero, Stringa),
        (Stringa, Numero, Stringa),
        (Stringa, Numero, Stringa, Numero, Stringa, Numero, Stringa)...
    )
    return = [Numero, Numero, Numero]
    """
    out: list[int] = []
    for row in matrix:
        for index, number in enumerate(cast(tuple[int, ...], row[1::2])):
            try:
                current_max = out[index]
            except IndexError:
                out.append(number)  # sarà di sicuro un off-by-one, non di più
            else:
                if number > current_max:
                    out[index] = number
    return out


def numero_cifre(number: int) -> int:
    """Get the number of digits needed for number (in base 10...)."""
    if number == 0:
        return 1
    return int(log10(number) + 1)


def rinomina(tupla: tuple[str | int, ...], digits: 'Sequence[int]') -> str:
    """Translate (Stringa, Intero, Stringa...) in a string.

    Use for each number the corresponding needed digits element.
    """
    ret = [cast(str, tupla[0])]
    i = 0
    while True:
        try:
            numero = cast(int, tupla[2 * i + 1])
        except IndexError:
            break
        digit = digits[i]
        stringa = tupla[2 * i + 2]
        ret.append('%0*d%s' % (digit, numero, stringa))
        i += 1
    return ''.join(ret)


def move(options: Values) -> 'Callable[[str, str], None]':
    def move_opted(file_from: str, file_to: str, /) -> None:
        if options.verbose:
            logger.info('%s -> %s', file_from, file_to)
        if Path(file_to).exists():
            warn(f'{file_to} è già usato!')
        elif not options.test:
            shmove(file_from, file_to)

    return move_opted


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    parser = OptionParser(
        version='%prog 0.1',
        usage="""%prog FILE...
    rinomina i file effettuando il padding dei numeri incontrati""",
    )
    parser.add_option(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='Mostra su STDOUT le azioni compiute',
    )
    parser.add_option(
        '-t',
        '--test',
        action='store_true',
        default=False,
        help="Non compiere nessuna rinomina (utile con '--verbose')",
    )

    options, args = parser.parse_args()
    if not args:
        parser.print_help()
        raise SystemExit
    # filenames è usato 2 volte
    filenames = list(filter(exists_warn, map(Path, args)))
    bases, names = zip(*map(split, filenames), strict=False)
    # names_with_integers è usato 2 volte
    names_with_integers = list(map(find_integers, names))
    # digits è usato un numero imprecisato di volte!
    digits = list(map(numero_cifre, multi_max(names_with_integers)))
    re_names = (rinomina(n, digits) for n in names_with_integers)
    destnames = starmap(join, zip(bases, re_names, strict=False))
    tuple(starmap(move(options), zip(filenames, destnames, strict=False)))


if __name__ == '__main__':
    main()
