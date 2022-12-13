

import socket
import sys
import struct

def decode_udp(data):
    data = data[0:12].decode('ascii')
    print(data)
    #print (repr (data))
    #var = struct.unpack('H',data[13:15])
    #print(var)
    #print("Size of String representation is {}.".format(struct.calcsize('h')))
    #print(var)

decode_udp(b'\xf8gxpP@2\x15\x00~\x0e\x19\x11\x01\xff\xff\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00')



# data_hex = '0xf867787050403215007e0e131301Ffff0000030000000000000000'

# def encode_udp(data_hex):
#     data_hex = data_hex.encode('d)
#     print(data_hex)


# encode_udp(data_hex)