from nose.tools import eq_, raises
from lnkrypto.util import int2hex, hex2int, hex2str, str2hex, int2str, str2int


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
        eq_(hex2int('27e41b3246bec9b16e398115'),
            12345678901234567890123456789)

    def test_hex2str(self):
        eq_(hex2str(''), '')
        eq_(hex2str('7375736869'), 'sushi')

    def test_str2hex(self):
        eq_(str2hex(''), '')
        eq_(str2hex('sushi'), '7375736869')

    def test_int2str(self):
        eq_(int2str(131260431295081), 'wasabi')

    @raises(ValueError)
    def test_int2str_invalid(self):
        int2str(-1)

    def test_str2int(self):
        eq_(str2int('wasabi'), 131260431295081)
