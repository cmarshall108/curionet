"""
 * Copyright (C) Caleb Marshall and others... - All Rights Reserved
 * Written by Caleb Marshall <anythingtechpro@gmail.com>, May 27th, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
"""

from curionet import io

data_buffer = io.DataBufferIO()

data_buffer.write_byte(1)

print (repr(data_buffer.remaining))
print (data_buffer.read_byte())

data_buffer.write_bool(True)
data_buffer.write_bool(False)

print (repr(data_buffer.remaining))
print (data_buffer.read_bool())
print (data_buffer.read_bool())

data_buffer.write_double(1.9999999)

print (repr(data_buffer.remaining))
print (data_buffer.read_double())

data_buffer.clear()

print (len(data_buffer.remaining))
