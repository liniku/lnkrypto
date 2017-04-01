from nose.tools import eq_
from lnkrypto.xorcipher import simple_xor


class TestXORCipher:
    def test_simple_xor(self):
        eq_(simple_xor(b'wabi-sabi', b'\x01'), b'v`ch,r`ch')
        eq_(simple_xor(b'wabi-sabi', b'\x01\x02'), b'vcck,q``h')
        eq_(simple_xor(b'wabi-sabi', b'wabi-sabi-dance'),
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00')
