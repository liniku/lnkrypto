import sys

if sys.version_info[0] >= 3:
    import binascii


def int2hex(i):
    if i < 0:
        raise ValueError('Input integer must be not negative.')

    h = hex(i)[2:].rstrip('L')
    if len(h) % 2 == 1:
        h = '0' + h
    return h


def hex2int(h):
    return int(h, 16)


if sys.version_info[0] >= 3:
    def str2bytes(s):
        return s.encode('utf-8')

    def bytes2str(b):
        return b.decode('utf-8')

    def hex2bytes(h):
        return bytes.fromhex(h)

    def bytes2hex(b):
        return bytes2str(binascii.hexlify(b))

    def hex2str(h):
        return bytes2str(hex2bytes(h))

    def str2hex(s):
        return bytes2hex(str2bytes(s))
else:
    def hex2str(h):
        return h.decode('hex')

    def str2hex(s):
        return s.encode('hex')


def int2str(i):
    return hex2str(int2hex(i))


def str2int(s):
    return hex2int(str2hex(s))
