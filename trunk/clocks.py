#!/usr/bin/env python
# -*- coding: utf-8 -*-

CLOCKS = [
    u'🕐', u'🕜',
    u'🕑', u'🕝',
    u'🕒', u'🕞',
    u'🕓', u'🕟',
    u'🕔', u'🕠',
    u'🕕', u'🕡',
    u'🕖', u'🕢',
    u'🕗', u'🕣',
    u'🕘', u'🕤',
    u'🕙', u'🕥',
    u'🕚', u'🕦',
    u'🕛', u'🕧'
]

def clocks(now):
    '''io ho HH:00, HH:30, HH+1:00

    se ho MM < 15 uso HH:00
    se ho 15 <= MM < 45 uso HH:30
    se ho 45 <= MM uso HH+1:00'''

    hour = now.hour
    minute = now.minute

    if minute < 15:
        return CLOCKS[(hour-1)*2%len(CLOCKS)]   # 1:00 è all'indice 0, 2:00 all'indice 2, 13:00 all'indice 0, 14:00 all'indice 2
    elif minute < 45:
        return CLOCKS[(hour-1)*2%len(CLOCKS)+1] # 1:30 è all'indice 1, 2:30 all' indice 3, 13:30 all'indice 1, 14:30 all'indice 3
    else:
        return CLOCKS[hour*2 % len(CLOCKS)] # possibile overflow alle 12:45

def main():
    import datetime

    print(clocks(datetime.datetime.now()).encode('utf8'))

if __name__ == '__main__':
    main()
