#!/usr/bin/env python3

import os
from lnkrypto.xorcipher import simple_xor


def load_plain(file_path):
    with open(file_path, 'rb') as f:
        p = f.read()
    return p


def save_cipher(c, file_path):
    with open(file_path, 'wb') as f:
        f.write(c)


def main():
    mydir = os.path.dirname(os.path.realpath(__file__))
    input_path = os.path.join(mydir, 'plain.txt')
    output_path = os.path.join(mydir, 'cipher.bin')

    with open(input_path, 'rb') as fin:
        p = fin.read()

    k = b'Can you see me!?'
    c = simple_xor(p, k)

    with open(output_path, 'wb') as fout:
        fout.write(c)


if __name__ == '__main__':
    main()
