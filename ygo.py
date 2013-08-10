#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from sys import argv
from struct import unpack
from array import array


def read_uint32(f):
    bytes = f.read(4)   # 32 = 4 * 8
    uint = unpack('I', bytes)[0]
    return uint


def read_decript_filename(f):
    file_name = array('c', f.read(256))

    # file_name è crittato??
    for j in range(256):
        for z in range(4):
            tmp = (ord(file_name[j]) & 1) << 7
            file_name[j] = chr(ord(file_name[j]) >> 1)
            file_name[j] = chr(ord(file_name[j]) + tmp)

    # drop trailing '\0'
    file_name = file_name[:file_name.index('\0')]

    return file_name.tostring().decode(u'ascii')


def dump(fn):
    with open(fn, u'rb') as f:
        header = f.read(8).decode(u'ascii')
        assert header == u'KCEJYUGI'

        file_count = read_uint32(f)
        for i in range(file_count):
            file_name = read_decript_filename(f)
            file_offset = read_uint32(f)
            file_size = read_uint32(f)
            size2 = read_uint32(f)  # inutile ?

            print(
                'name: %s, offset: %s, size: %s, size2: %s' %
                (file_name, file_offset, file_size, size2)
            )


def main():
    fn = argv[1]
    dump(fn)

if __name__ == '__main__':
    main()
