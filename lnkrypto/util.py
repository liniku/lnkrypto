def int2hex(i):
    if i < 0:
        raise ValueError('Input integer must be not negative.')

    h = hex(i)[2:].rstrip('L')
    if len(h) % 2 == 1:
        h = '0' + h
    return h


def hex2int(h):
    return int(h, 16)


def hex2str(h):
    return h.decode('hex')


def str2hex(s):
    return s.encode('hex')


def int2str(i):
    return hex2str(int2hex(i))


def str2int(s):
    return hex2int(str2hex(s))
