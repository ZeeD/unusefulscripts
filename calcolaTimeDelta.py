#!/usr/bin/env python

from datetime import datetime

def parse_input(string):
    year,month,day_hour,minutes,seconds = string.split(':')
    day,hour = day_hour.split(' ')
    year,month,day,hour,minutes,seconds = [int(el) for el in year,month,day,hour,minutes,seconds]
    return year,month,day,hour,minutes,seconds

def main():
    from sys import argv
    if len(argv) > 1:
        first_date = datetime(*parse_input(argv[1]))
    else:
        first_date = datetime(*parse_input(raw_input()))
    print "%s (+ 0)" % first_date
    while True:
        try:
            second_date = datetime(*parse_input(raw_input()))
        except EOFError:
            break
        print "%s (+ %s)" % (second_date, second_date - first_date)
        first_date = second_date

if __name__ == '__main__':
    main()
