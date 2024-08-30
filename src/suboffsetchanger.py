from datetime import UTC
from datetime import datetime
from datetime import timedelta
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path
from shutil import copy
from sys import argv

logger = getLogger(__name__)


"""
id
datetime --> datetime (see TIME_FMT)
string
string
(empty)
"""

SPLITTER = ' --> '
TIME_FMT = '%H:%M:%S,%f'


def offset_changer(filename: str, offset: timedelta) -> None:
    infn = filename + '~'
    outfn = filename
    copy(outfn, infn)
    with Path(infn).open() as infile, Path(outfn).open('w') as outfile:
        while True:
            try:
                outfile.write(next(infile))
            except StopIteration:
                break

            subtitle_time = next(infile).strip()
            start_orig, end_orig = subtitle_time.split(SPLITTER)
            start_dt, end_dt = (
                datetime.strptime(start_orig, TIME_FMT).astimezone(tz=UTC),
                datetime.strptime(end_orig, TIME_FMT).astimezone(tz=UTC),
            )
            if (start_dt + offset).year >= 1900:  # noqa: PLR2004
                start_dt, end_dt = start_dt + offset, end_dt + offset
            start_new, end_new = (
                start_dt.strftime(TIME_FMT)[:-3],
                end_dt.strftime(TIME_FMT)[:-3],
            )
            subtitle_time = SPLITTER.join([start_new, end_new])
            outfile.write(subtitle_time + '\n')

            while True:
                message = next(infile)
                outfile.write(message)
                if not message.strip():
                    break


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
    try:
        _, filename, offset_raw = argv
    except ValueError:
        logger.error('Uso: %s filename offset', argv[0])  # noqa: TRY400
        raise SystemExit from None

    offset = timedelta(seconds=int(offset_raw))
    offset_changer(filename, offset)


if __name__ == '__main__':
    main()
