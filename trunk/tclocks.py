#!/usr/bin/env python

from __future__ import print_function

import clocks
import UnicodeName
import datetime

def main():
    fifteen_minutes = datetime.timedelta(minutes=15)

    t = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 10))
    t1 = t + datetime.timedelta(2)
    while t < t1:
        tt = t.time()
        print(tt, end=':', flush=True)
        c = clocks.clocks(tt)
        print(c, end=' [', flush=True)
        n = next(UnicodeName.data(c))[3]
        print(n, end=']\n', flush=True)

        t += fifteen_minutes

if __name__ == '__main__':
    main()
