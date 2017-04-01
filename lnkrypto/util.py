import binascii


def int2bytes(i, min_length=1):
    if min_length < 1:
        raise ValueError('min_length must be postiive integer.')
    return i.to_bytes(max((i.bit_length() + 7) // 8, min_length),
                      byteorder='big')


def bytes2int(b):
    return int.from_bytes(b, byteorder='big')


def str2bytes(s):
    return s.encode('utf-8')


def bytes2str(b):
    return b.decode('utf-8')


def hex2bytes(h):
    return bytes.fromhex(h)


def bytes2hex(b):
    return bytes2str(binascii.hexlify(b))


def int2hex(i):
    return bytes2hex(int2bytes(i))


def hex2int(h):
    return bytes2int(hex2bytes(h))


def hex2str(h):
    return bytes2str(hex2bytes(h))


def str2hex(s):
    return bytes2hex(str2bytes(s))


def int2str(i):
    return bytes2str(int2bytes(i))


def str2int(s):
    return bytes2int(str2bytes(s))
