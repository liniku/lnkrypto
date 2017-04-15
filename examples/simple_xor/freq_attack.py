#!/usr/bin/env python3

import os
from lnkrypto.util import bytes2str
from lnkrypto.xorcipher import simple_xor_freq_attack


def main():
    mydir = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(mydir, 'cipher.bin')

    with open(input_path, 'rb') as fin:
        c = fin.read()

    r = simple_xor_freq_attack(c, 30)

    if r is None:
        print('Freq attack failed :(')
    else:
        k, p = r
        print('Plain text:')
        print(bytes2str(p))
        print('Key:', bytes2str(k))


if __name__ == '__main__':
    main()
