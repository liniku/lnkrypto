import binascii

DEFAULT_SYMBOL_COVERAGE_THRES = 0.25


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


def printable_ascii(b):
    for c in b:
        if (c < 32 or c > 126) and c != 9 and c != 10:
            return False
    return True


def human_can_read_en(b,
                      symbol_coverage_thres=DEFAULT_SYMBOL_COVERAGE_THRES):
    if not printable_ascii(b):
        return False

    # count [^ .-,0-9a-zA-Z]
    s = 0
    for c in b:
        if c != 32 and (c < 44 or c > 46) \
                and (c < 48 or c > 57) \
                and (c < 65 or c > 90) \
                and (c < 97 or c > 122):
            s += 1
    if (s / len(b)) >= symbol_coverage_thres:
        return False
    return True


def hamming_distance(b1, b2):
    if len(b1) != len(b2):
        raise ValueError('Length of two bytes are different.')

    r = 0
    for c1, c2 in zip(b1, b2):
        x = c1 ^ c2
        while x > 0:
            r += x & 1
            x >>= 1

    return r
