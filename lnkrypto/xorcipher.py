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
    if key_length < 0:
        raise ValueError('Key length must be postive value.')

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


def simple_xor_crib_attack_fixed_length(c,
                                        crib,
                                        key_length,
                                        common_bytes=COMMON_BYTES_EN,
                                        plain_check_func=human_can_read_en):
    if key_length < 0:
        raise ValueError('Key length must be postive value.')

    crib_length = len(crib)
    for i in range(len(c) - crib_length):
        # restore a key from the crib
        key_restored = True
        k = [-1] * key_length
        for j in range(crib_length):
            t = c[i + j] ^ crib[j]
            p = (i + j) % key_length
            if k[p] < 0:
                k[p] = t
            elif k[p] != t:
                # the key restored from the crib is not consistent
                key_restored = False
                break
        if not key_restored:
            continue

        # check the key is valid
        check_passed = True
        for j in range(key_length):
            if k[j] < 0:
                continue
            if not plain_check_func(simple_xor(c[j::key_length],
                                               int2bytes(k[j]))):
                check_passed = False
                break

        # retrun key, plaintext (partially decoded) and mask
        if check_passed:
            mask = []
            for j in range(len(k)):
                if k[j] < 0:
                    k[j] = 0
                    mask.append(False)
                else:
                    mask.append(True)
            k = bytes(k)
            p = simple_xor(c, k)
            return k, p, mask
