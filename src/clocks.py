#!/usr/bin/env python

from datetime import datetime
from logging import INFO
from logging import basicConfig
from logging import info

CLOCKS = '🕐🕜🕑🕝🕒🕞🕓🕟🕔🕠🕕🕡🕖🕢🕗🕣🕘🕤🕙🕥🕚🕦🕛🕧'

QUARTER = 15
THREE_QUARTERS = 45


def clocks(now: datetime) -> str:
    """Io ho HH:00, HH:30, HH+1:00 .

    se ho MM < 15 uso HH:00
    se ho 15 <= MM < 45 uso HH:30
    se ho 45 <= MM uso HH+1:00
    """
    hour = now.hour
    minute = now.minute

    if minute < QUARTER:
        # 1:00 è all'indice 0, 2:00 all'indice 2,
        # 13:00 all'indice 0, 14:00 all'indice 2
        return CLOCKS[(hour - 1) * 2 % len(CLOCKS)]

    if minute < THREE_QUARTERS:
        # 1:30 è all'indice 1, 2:30 all' indice 3,
        # 13:30 all'indice 1, 14:30 all'indice 3
        return CLOCKS[(hour - 1) * 2 % len(CLOCKS) + 1]

    # possibile overflow alle 12:45
    return CLOCKS[hour * 2 % len(CLOCKS)]


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    info(clocks(datetime.now()))


if __name__ == '__main__':
    main()
