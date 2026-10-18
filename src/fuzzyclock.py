from datetime import datetime
from datetime import time
from logging import INFO
from logging import basicConfig
from logging import getLogger
from typing import Final
from zoneinfo import ZoneInfo

TZ: Final = ZoneInfo('Europe/Rome')
logger: Final = getLogger(__name__)


def _fuzzyhour(hh: int) -> str:
    return [
        'mezzanotte',
        'una',
        'due',
        'tre',
        'quattro',
        'cinque',
        'sei',
        'sette',
        'otto',
        'nove',
        'dieci',
        'undici',
        'dodici',
        'una',
        'due',
        'tre',
        'quattro',
        'cinque',
        'sei',
        'sette',
        'otto',
        'nove',
        'dieci',
        'undici',
    ][hh]


def _fuzzyminute(mm: int) -> tuple[str, bool]:
    return [
        ('', False),
        (' e cinque', False),
        (' e dieci', False),
        (' e un quarto', False),
        (' e venti', False),
        (' e venticinque', False),
        (' e mezza', False),
        (' e trentacinque', False),
        (' meno venti', True),
        (' meno un quarto', True),
        (' meno dieci', True),
        (' meno cinque', True),
    ][mm // 5]


def fuzzyclock(now: time) -> str:
    fmt_mm, next_hour = _fuzzyminute(now.minute)
    hh = (now.hour + 1) % 24 if next_hour else now.hour
    fmt_hh = _fuzzyhour(hh)
    return f'{fmt_hh}{fmt_mm}'


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    now = datetime.now(tz=TZ).time()
    logger.info('%s', fuzzyclock(now))


if __name__ == '__main__':
    main()
