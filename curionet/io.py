"""
 * Copyright (C) Caleb Marshall and others... - All Rights Reserved
 * Written by Caleb Marshall <anythingtechpro@gmail.com>, May 27th, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
"""

import struct

class Endianness(object):
    """
    A enum that stores network endianess formats
    """

    NATIVE = '='
    LITTLE_ENDIAN = '<'
    BIG_ENDIAN = '>'
    NETWORK = '!'

class DataBufferError(IOError):
    """
    A data buffer specific io error
    """

class DataBufferIO(object):
    """
    A class for manipulating (reading and/or writing) an array of bytes
    """

    BYTE_ORDER = Endianness.NETWORK

    def __init__(self, data=bytes(), offset=0):
        self.data = data
        self.offset = offset

    @property
    def byte_order(self):
        return self.BYTE_ORDER

    @property
    def remaining(self):
        return self.data[self.offset:]

    def read(self, length):
        data = self.remaining[:length]
        self.offset += length
        return data

    def write(self, data):
        if not data:
            return

        self.data += data

    def clear(self):
        self.data = bytes()
        self.offset = 0

    def read_from(self, fmt):
        data = struct.unpack_from(self.byte_order + fmt, self.data, self.offset)
        self.offset += struct.calcsize(fmt)
        return data

    def write_to(self, fmt, *args):
        self.write(struct.pack(self.byte_order + fmt, *args))

    def read_byte(self):
        return self.read_from('b')[0]

    def write_byte(self, value):
        self.write_to('b', value)

    def read_ubyte(self):
        return self.read_from('B')[0]

    def write_ubyte(self, value):
        self.write_to('B', value)

    def read_bool(self):
        return self.read_from('?')[0]

    def write_bool(self, value):
        self.write_to('?', value)

    def read_short(self):
        return self.read_from('h')[0]

    def write_short(self, value):
        self.write_to('h', value)

    def read_ushort(self):
        return self.read_from('H')[0]

    def write_ushort(self, value):
        self.write_to('H', value)

    def read_int(self):
        return self.read_from('i')[0]

    def write_int(self, value):
        self.write_to('i', value)

    def read_uint(self):
        return self.read_from('I')[0]

    def write_uint(self, value):
        self.write_to('I', value)

    def read_long(self):
        return self.read_from('l')[0]

    def write_long(self, value):
        self.write_to('l', value)

    def read_ulong(self):
        return self.read_from('L')[0]

    def write_ulong(self, value):
        self.write_to('L', value)

    def read_long_long(self):
        return self.read_from('q')[0]

    def write_long_long(self, value):
        self.write_to('q', value)

    def read_ulong_long(self):
        return self.read_from('Q')[0]

    def write_ulong_long(self, value):
        self.write_to('Q', value)

    def read_float(self):
        return self.read_from('f')[0]

    def write_float(self, value):
        self.write_to('f', value)

    def read_double(self):
        return self.read_from('d')[0]

    def write_double(self, value):
        self.write_to('d', value)

    def read_char(self):
        return self.read_from('s')[0]

    def write_char(self, value):
        self.write_to('s', value)
