from nose.tools import eq_, ok_
from lnkrypto.xorcipher import \
    simple_xor, \
    simple_xor_freq_attack_single_byte, \
    simple_xor_freq_attack_fixed_length, \
    simple_xor_freq_attack, \
    simple_xor_crib_attack_fixed_length


class TestXORCipher:
    def test_simple_xor(self):
        eq_(simple_xor(b'wabi-sabi', b'\x01'), b'v`ch,r`ch')
        eq_(simple_xor(b'wabi-sabi', b'\x01\x02'), b'vcck,q``h')
        eq_(simple_xor(b'wabi-sabi', b'wabi-sabi-dance'),
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_simple_xor_attck_single_byte(self):
        k, p = simple_xor_freq_attack_single_byte(
            b"\x1c.k<.9.k=.92k'>( 2k?$k8..k?#*?e")
        eq_(k, b'K')
        eq_(p, b'We were very lucky to see that.')

    def test_simple_xor_freq_attack_fixed_length(self):
        k1, p1 = simple_xor_freq_attack_fixed_length(
            b"\x1c.k<.9.k=.92k'>( 2k?$k8..k?#*?e", 1)
        eq_(k1, b'K')
        eq_(p1, b'We were very lucky to see that.')
        k2, p2 = simple_xor_freq_attack_fixed_length(
            b'tV\x03DFAF\x13UVQJ\x03_VPHJ\x03GL\x13PVF\x13W[BG\r', 2)
        eq_(k2, b'#3')
        eq_(p2, b'We were very lucky to see that.')

    def test_simple_xor_freq_attack(self):
        key = b'Oops'
        plaintext = \
            b"Cruel and sudden, hast thou since Purpled thy nail in blood " \
            b"of innocence? Wherein could this flea guilty be, Except in th" \
            b"at drop which it suck'd from thee?"
        ciphertext = \
            b'\x0c\x1d\x05\x16\x23\x4f\x11\x1d\x2b\x4f\x03\x06' \
            b'\x2b\x0b\x15\x1d\x63\x4f\x18\x12\x3c\x1b\x50\x07' \
            b'\x27\x00\x05\x53\x3c\x06\x1e\x10\x2a\x4f\x20\x06' \
            b'\x3d\x1f\x1c\x16\x2b\x4f\x04\x1b\x36\x4f\x1e\x12' \
            b'\x26\x03\x50\x1a\x21\x4f\x12\x1f\x20\x00\x14\x53' \
            b'\x20\x09\x50\x1a\x21\x01\x1f\x10\x2a\x01\x13\x16' \
            b'\x70\x4f\x27\x1b\x2a\x1d\x15\x1a\x21\x4f\x13\x1c' \
            b'\x3a\x03\x14\x53\x3b\x07\x19\x00\x6f\x09\x1c\x16' \
            b'\x2e\x4f\x17\x06\x26\x03\x04\x0a\x6f\x0d\x15\x5f' \
            b'\x6f\x2a\x08\x10\x2a\x1f\x04\x53\x26\x01\x50\x07' \
            b'\x27\x0e\x04\x53\x2b\x1d\x1f\x03\x6f\x18\x18\x1a' \
            b'\x2c\x07\x50\x1a\x3b\x4f\x03\x06\x2c\x04\x57\x17' \
            b'\x6f\x09\x02\x1c\x22\x4f\x04\x1b\x2a\x0a\x4f'
        r = simple_xor_freq_attack(ciphertext, max_key_length=2)
        ok_(r is None)
        k, p = simple_xor_freq_attack(ciphertext, max_key_length=6)
        eq_(k, key)
        eq_(p, plaintext)

    def test_simple_xor_crib_attack_fixed_length(self):
        ciphertext = b'=\x10N\x1c\x0f\x07\x0bK\x1c\x10\x1c\x12J\x19'\
            b'\x1b\x08\x01\x0cN\x1f\x05U\x1d\x0e\x0fU\x1a\x03\x0b\x01@'

        k1, p1, m1 = simple_xor_crib_attack_fixed_length(ciphertext,
                                                         b' to ', 4)
        eq_(k1, b'junk')
        eq_(p1, b'We were very lucky to see that.')
        eq_(m1, [True, True, True, True])

        k2, p2, m2 = simple_xor_crib_attack_fixed_length(ciphertext,
                                                         b' lu', 4)
        eq_(k2, b'jun\x00')
        eq_(p2, b'We \x1cereKver\x12 lu\x08ky \x1fo s\x0ee t\x03at.')
        eq_(m2, [True, True, True, False])

        r1 = simple_xor_crib_attack_fixed_length(ciphertext, b'zx', 4)
        eq_(r1, None)

        r2 = simple_xor_crib_attack_fixed_length(ciphertext,
                                                 b'We were lucky', 4)
        eq_(r2, None)
