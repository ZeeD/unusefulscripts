from itertools import groupby
from logging import INFO
from logging import basicConfig
from logging import getLogger
from optparse import OptionParser
from optparse import Values
from typing import TYPE_CHECKING

from pypdf import PdfReader

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = getLogger(__name__)


def raggruppamenti(total_pages: int) -> 'Iterable[tuple[int, int]]':
    group_pages = 0
    while group_pages < total_pages:
        groups_len = 0
        group_pages += 4
        while groups_len * group_pages < total_pages:
            groups_len += 1
        yield group_pages, groups_len


def print_one_row(
    headers_l: list[int], format_: str, pt: int, ppr: int, nr: int
) -> None:
    ps = ppr * nr
    elements = (ppr, nr, ps, pt, ps - pt)
    logger.info(
        format_,
        ('%d (== 4x%d)' % (elements[0], elements[0] / 4)).center(headers_l[0]),
        *(
            str(n).center(len_)
            for n, len_ in list(zip(elements, headers_l, strict=False))[1:]
        ),
    )


def print_output(
    headers: tuple[str, ...],
    format_: str,
    total_pages: int,
    *,
    show_all: bool = False,
) -> None:
    logger.info(format_, *headers)
    logger.info('-' * (sum(map(len, headers)) + len(format_)))
    headers_l = list(map(len, headers))
    if show_all:
        for group_pages, groups_len in raggruppamenti(total_pages):
            print_one_row(
                headers_l, format_, total_pages, group_pages, groups_len
            )
    else:
        for group_pages, groups_len in (
            min(el[1])
            for el in groupby(raggruppamenti(total_pages), lambda e: e[1])
        ):
            print_one_row(
                headers_l, format_, total_pages, group_pages, groups_len
            )


def parse_args() -> tuple[Values, list[str]]:
    parser = OptionParser(
        version='%prog 0.4.0',
        usage="""%prog [PDF|NUMERO]...
        Genera le possibili combinazioni per stampare NUMERO pagine
        (eventualmente estratte dal PDF)""",
    )
    parser.add_option(
        '-a',
        '--all',
        action='store_true',
        default=False,
        help='Mostra tutte le possibili combinazioni',
    )
    options, args = parser.parse_args()
    if not args:
        parser.print_usage()
        raise SystemExit
    return options, args


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    options, args = parse_args()
    headers = (
        'pagine_per_raggruppamento',
        'numero_raggruppamenti',
        'pagine_stampate',
        'pagine_totali',
        'bianche',
    )

    for arg in args:
        try:
            total_pages = int(arg)
        except ValueError:
            try:
                total_pages = PdfReader(arg).get_num_pages()
            except FileNotFoundError:
                msg = f'{arg!r} must be a number or a pdf'
                raise RuntimeWarning(msg) from None

        print_output(
            headers,
            '%s * %s == %s == %s + %s',
            total_pages,
            show_all=options.all,
        )


if __name__ == '__main__':
    main()
