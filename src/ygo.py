#!/usr/bin/env python

from array import array
from struct import unpack
from sys import argv


def read_uint32(f):
    bytes = f.read(4)  # 32 = 4 * 8
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
    file_name = file_name[: file_name.index('\0')]

    return file_name.tostring().decode('ascii')


def dump(fn):
    with open(fn, 'rb') as f:
        header = f.read(8).decode('ascii')
        assert header == 'KCEJYUGI'

        file_count = read_uint32(f)
        for i in range(file_count):
            file_name = read_decript_filename(f)
            file_offset = read_uint32(f)
            file_size = read_uint32(f)
            size2 = read_uint32(f)  # inutile ?

            print(
                'name: %s, offset: %s, size: %s, size2: %s'
                % (file_name, file_offset, file_size, size2)
            )


def main():
    fn = argv[1]
    dump(fn)


if __name__ == '__main__':
    main()
