import collections
from lnkrypto.util import int2bytes, human_can_read_en, hamming_distance

COMMON_BYTES_EN = b' etaoinshrdlu'


def simple_xor(p, k):
    l = len(k)
    c = [x ^ k[i % l] for i, x in enumerate(p)]
    return bytes(c)


def simple_xor_freq_attack_single_byte(c,
                                       common_bytes=COMMON_BYTES_EN,
                                       plain_check_func=human_can_read_en):
    counter = collections.Counter(c)
    most_common_byte = counter.most_common(1)[0][0]
    for x in common_bytes:
        k = int2bytes(most_common_byte ^ x)
        p = simple_xor(c, k)
        if plain_check_func(p):
            return k, p


def simple_xor_freq_attack_fixed_length(c,
                                        key_length,
                                        common_bytes=COMMON_BYTES_EN,
                                        plain_check_func=human_can_read_en):
    key = []
    for i in range(key_length):
        b = c[i::key_length]
        r = simple_xor_freq_attack_single_byte(b, common_bytes,
                                               plain_check_func)
        if r is None:
            break
        key.append(ord(r[0]))
    if len(key) != key_length:
        return None
    key = bytes(key)
    p = simple_xor(c, key)
    return key, p


def simple_xor_freq_attack(c,
                           max_key_length,
                           common_bytes=COMMON_BYTES_EN,
                           plain_check_func=human_can_read_en):
    # calculate the (approximate) average hamming distance for each blocks
    h = []
    for key_length in range(1, max_key_length + 1):
        num_blocks = len(c) // key_length
        s = 0
        for i in range(num_blocks - 1):
            b1 = c[i*key_length:(i+1)*key_length]
            b2 = c[(i+1)*key_length:(i+2)*key_length]
            s += hamming_distance(b1, b2)
        h.append((s / ((num_blocks - 1) * key_length), key_length))
    h.sort()

    # key length with the minimum hamming distance is likely to be correct
    for _, key_length in h:
        r = simple_xor_freq_attack_fixed_length(c, key_length,
                                                common_bytes, plain_check_func)
        if r is not None:
            return r
