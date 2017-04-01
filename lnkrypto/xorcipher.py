def simple_xor(p, k):
    l = len(k)
    c = [x ^ k[i % l] for i, x in enumerate(p)]
    return bytes(c)
