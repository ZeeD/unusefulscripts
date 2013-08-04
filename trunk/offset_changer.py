#!/usr/bin/env python

from sys import argv
from datetime import timedelta
from shutil import copy
from datetime import datetime

'''
id
datetime --> datetime (see TIME_FMT)
string
string
(empty)
'''

SPLITTER = ' --> '
TIME_FMT = '%H:%M:%S,%f'


def offset_changer(filename, offset):
    infn = filename + '~'
    outfn = filename
    copy(outfn, infn)
    with open(infn) as infile, open(outfn, 'w') as outfile:
        while True:
            try:
                outfile.write(next(infile))
            except StopIteration:
                break

            subtitle_time = next(infile).strip()
            start, end = subtitle_time.split(SPLITTER)
            start, end = (
                datetime.strptime(start, TIME_FMT),
                datetime.strptime(end, TIME_FMT)
            )
            if (start + offset).year >= 1900:
                start, end = start + offset, end + offset
            start, end = (
                start.strftime(TIME_FMT)[:-3],
                end.strftime(TIME_FMT)[:-3]
            )
            subtitle_time = SPLITTER.join([start, end])
            outfile.write(subtitle_time + '\n')

            while True:
                message = next(infile)
                outfile.write(message)
                if not message.strip():
                    break


def main():
    if len(argv) < 3:
        raise SystemExit('Uso: %s filename offset' % (argv[0], ))

    filename = argv[1]
    offset = timedelta(seconds=int(argv[2]))
    offset_changer(filename, offset)

if __name__ == '__main__':
    main()
