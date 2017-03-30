from nose.tools import eq_, raises
from lnkrypto.util import int2hex, hex2int


class TestUtil:
    def test_int2hex_short(self):
        eq_(int2hex(0), '00')
        eq_(int2hex(16), '10')
        eq_(int2hex(257), '0101')

    def test_int2hex_long(self):
        eq_(int2hex(12345678901234567890123456789),
            '27e41b3246bec9b16e398115')
        eq_(int2hex(123456789012345678901234567890),
            '018ee90ff6c373e0ee4e3f0ad2')

    @raises(ValueError)
    def test_int2hex_invalid(self):
        int2hex(-1)

    def test_hex2int(self):
        eq_(hex2int('00'), 0)
        eq_(hex2int('1234'), 4660)
