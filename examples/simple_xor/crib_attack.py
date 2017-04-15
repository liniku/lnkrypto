#!/usr/bin/env python3

import os
from lnkrypto.util import str2bytes, bytes2str
from lnkrypto.xorcipher import simple_xor_crib_attack_fixed_length


def mask_bytes(b, m):
    s = []
    for i in range(len(b)):
        if m[i]:
            s.append(b[i])
        else:
            s.append(95)  # '_'
    return bytes(s)


def show_hint(k, p, m):
    print('Plain text:')
    for i in range(0, len(p), len(k)):
        print(bytes2str(mask_bytes(p[i:i+len(k)], m)),)
    print('Key:', bytes2str(mask_bytes(k, m)))


def main():
    mydir = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(mydir, 'cipher.bin')

    with open(input_path, 'rb') as fin:
        c = fin.read()

    succeeded = False
    while True:
        crib = str2bytes(input('crib (Enter empty line to quit): '))
        if crib == b'':
            break
        # suppose that we know key length
        r = simple_xor_crib_attack_fixed_length(c, crib, 16)
        if r is None:
            print('Crib attack failed :(')
        else:
            k, p, m = r
            if all(m):
                succeeded = True
                break
            show_hint(k, p, m)

    if succeeded:
        print('Plain text:')
        print(bytes2str(p))
        print('Key:', bytes2str(k))
    else:
        print('Crib attack failed :(')


if __name__ == '__main__':
    main()
