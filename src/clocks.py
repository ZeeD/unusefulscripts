from datetime import datetime
from datetime import time
from logging import INFO
from logging import basicConfig
from logging import getLogger
from typing import Final
from zoneinfo import ZoneInfo

CLOCKS: Final = [
    '🕐',
    '🕜',
    '🕑',
    '🕝',
    '🕒',
    '🕞',
    '🕓',
    '🕟',
    '🕔',
    '🕠',
    '🕕',
    '🕡',
    '🕖',
    '🕢',
    '🕗',
    '🕣',
    '🕘',
    '🕤',
    '🕙',
    '🕥',
    '🕚',
    '🕦',
    '🕛',
    '🕧',
]
QUARTER: Final = 15
THREE_QUARTERS: Final = 45
TZ: Final = ZoneInfo('Europe/Rome')

logger: Final = getLogger(__name__)


def clocks(now: time) -> str:
    """Io ho HH:00, HH:30, HH+1:00 .

    se ho MM < 15 uso HH:00
    se ho 15 <= MM < 45 uso HH:30
    se ho 45 <= MM uso HH+1:00
    """
    hour = now.hour
    minute = now.minute

    if minute < QUARTER:
        # 01:00 è all'indice 0, 02:00 all'indice 2
        # 13:00 è all'indice 0, 14:00 all'indice 2
        return CLOCKS[(hour - 1) * 2 % len(CLOCKS)]

    if minute < THREE_QUARTERS:
        # 01:30 è all'indice 1, 02:30 all'indice 3
        # 13:30 è all'indice 1, 14:30 all'indice 3
        return CLOCKS[(hour - 1) * 2 % len(CLOCKS) + 1]

    # possibile overflow alle 12:45
    return CLOCKS[hour * 2 % len(CLOCKS)]


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    now = datetime.now(tz=TZ).time()
    clock = clocks(now)
    logger.info('%s', clock)


if __name__ == '__main__':
    main()
