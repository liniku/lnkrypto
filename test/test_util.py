from nose.tools import eq_, ok_, raises
from lnkrypto.util import \
    int2bytes, \
    bytes2int, \
    str2bytes, \
    bytes2str, \
    hex2bytes, \
    bytes2hex, \
    int2hex, \
    hex2int, \
    hex2str, \
    str2hex, \
    int2str, \
    str2int, \
    printable_ascii, \
    human_can_read_en, \
    hamming_distance


class TestUtil:
    def test_str2bytes(self):
        eq_(str2bytes(''), b'')
        eq_(str2bytes('\x12\x34'), b'\x12\x34')
        eq_(str2bytes('sushi'), b'sushi')

    def bytes2str(self):
        eq_(bytes2str(b''), '')
        eq_(bytes2str(b'\x12\x34'), '\x12\x34')
        eq_(bytes2str(b'sushi'), 'sushi')

    def test_hex2bytes(self):
        eq_(hex2bytes(''), b'')
        eq_(hex2bytes('00'), b'\x00')
        eq_(hex2bytes('0000'), b'\x00\x00')
        eq_(hex2bytes('0213'), b'\x02\x13')
        eq_(hex2bytes('7375736869'), b'sushi')

    @raises(ValueError)
    def test_hex2bytes_invalid(self):
        hex2bytes('213')

    def test_bytes2hex(self):
        eq_(bytes2hex(b''), '')
        eq_(bytes2hex(b'\x00'), '00')
        eq_(bytes2hex(b'\x00\x00'), '0000')
        eq_(bytes2hex(b'\x02\x13'), '0213')
        eq_(bytes2hex(b'sushi'), '7375736869')

    def test_int2bytes(self):
        eq_(int2bytes(0), b'\x00')
        eq_(int2bytes(1), b'\x01')
        eq_(int2bytes(4627), b'\x12\x13')
        eq_(int2bytes(131260431295081), b'wasabi')

    def test_int2bytes_min_length(self):
        eq_(int2bytes(0, min_length=3), b'\x00\x00\x00')
        eq_(int2bytes(131260431295081, min_length=3), b'wasabi')
        eq_(int2bytes(131260431295081, min_length=9), b'\x00\x00\x00wasabi')

    @raises(ValueError)
    def test_int2bytes_invalid_min_length(self):
        int2bytes(1000, min_length=-1)

    @raises(OverflowError)
    def test_int2bytes_invalid(self):
        int2bytes(-1)

    def test_bytes2int(self):
        eq_(bytes2int(b''), 0)
        eq_(bytes2int(b'\x00'), 0)
        eq_(bytes2int(b'\x00\x00'), 0)
        eq_(bytes2int(b'\x01'), 1)
        eq_(bytes2int(b'\x12\x13'), 4627)
        eq_(bytes2int(b'wasabi'), 131260431295081)

    def test_int2hex(self):
        eq_(int2hex(0), '00')
        eq_(int2hex(1), '01')
        eq_(int2hex(16), '10')
        eq_(int2hex(257), '0101')
        eq_(int2hex(12345678901234567890123456789),
            '27e41b3246bec9b16e398115')
        eq_(int2hex(123456789012345678901234567890),
            '018ee90ff6c373e0ee4e3f0ad2')

    @raises(OverflowError)
    def test_int2hex_invalid(self):
        int2hex(-1)

    def test_hex2int(self):
        eq_(hex2int(''), 0)
        eq_(hex2int('00'), 0)
        eq_(hex2int('1234'), 4660)
        eq_(hex2int('27e41b3246bec9b16e398115'),
            12345678901234567890123456789)

    @raises(ValueError)
    def test_hex2int_invalid(self):
        hex2int('123')

    def test_hex2str(self):
        eq_(hex2str(''), '')
        eq_(hex2str('00'), '\x00')
        eq_(hex2str('0000'), '\x00\x00')
        eq_(hex2str('7375736869'), 'sushi')

    def test_str2hex(self):
        eq_(str2hex(''), '')
        eq_(str2hex('\x00'), '00')
        eq_(str2hex('\x00\x00'), '0000')
        eq_(str2hex('sushi'), '7375736869')

    def test_int2str(self):
        eq_(int2str(0), '\x00')
        eq_(int2str(131260431295081), 'wasabi')

    @raises(OverflowError)
    def test_int2str_invalid(self):
        int2str(-1)

    def test_str2int(self):
        eq_(str2int('wasabi'), 131260431295081)

    def test_printable_ascii(self):
        ok_(printable_ascii(b'maguro'))
        ok_(printable_ascii(b'!"#$%&\'()=~|`{+*}<>?_-^\\@[;:],./'))
        ok_(printable_ascii(b'a\nb\tc'))
        ok_(not printable_ascii(b'abcdefg\x03'))

    def test_human_can_read_en(self):
        ok_(not human_can_read_en(b'ab.*^-32++'))
        ok_(human_can_read_en(b'ab.*^-32++',
                              symbol_coverage_thres=0.8))

    def test_hamming_distance(self):
        eq_(hamming_distance(b'\x12\x34', b'\x17\x84'), 5)
        eq_(hamming_distance(b'wabi', b'sabi'), 1)

    @raises(ValueError)
    def test_hamming_distance_invalid(self):
        hamming_distance(b'wabi', b'wasabi')
