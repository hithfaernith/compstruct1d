import math
import copy


class BinNumber(object):
    def __init__(
        self, num, num_bits=32, hex_val=None,
        signed=True, editable=False
    ):
        self.num_bits = num_bits
        self.signed = signed
        self.editable = editable

        if type(num) == list:
            self.bits = copy.deepcopy(num)
            assert len(self.bits) == num_bits
        else:
            if num < 0:
                assert signed
                negative = True
                num = num + 2 ** (num_bits - 1)
            else:
                negative = False

            self.bits = self.fill_bits(
                num, num_bits=num_bits, negative=negative
            )

        if hex_val is not None:
            assert hex_val == self.to_decimal(
                self.bits, False
            )

    def enable_edit(self):
        self.editable = True
        return self

    def disable_edit(self):
        self.editable = False
        return self

    def __int__(self):
        return self.value

    @staticmethod
    def _sra(x, n, m):
        # shift x of n bits right by m
        if x & 2 ** (n - 1) != 0:  # MSB is 1, i.e. x is negative
            filler = int('1' * m + '0' * (n - m), 2)
            x = (x >> m) | filler  # fill in 0's with 1's
            return x
        else:
            return x >> m

    @staticmethod
    def _sla(x, n, m):
        # shift x of n bits left by m
        if x & 2 ** (n - 1) != 0:  # MSB is 1, i.e. x is negative
            filler = int('1' * m + '0' * (n - m), 2)
            x = (x << m) | filler  # fill in 0's with 1's
            return x
        else:
            return x << m

    def shift_right_arith(self, bits):
        if isinstance(bits, BinNumber):
            bits = bits.value

        value = self._sra(self.value, self.num_bits, bits)
        return self.__class__(
            num=value, num_bits=self.num_bits,
            signed=self.signed
        )

    def zero_all_bits(self):
        assert self.editable
        for k in range(len(self)):
            self[k] = 0

    def shift_left_arith(self, bits):
        if isinstance(bits, BinNumber):
            bits = bits.value

        value = self._sla(self.value, self.num_bits, bits)
        return self.__class__(
            num=value, num_bits=self.num_bits,
            signed=self.signed
        )

    def to_signed(self):
        bits = copy.deepcopy(self.bits)
        return self.__class__(
            num=bits, num_bits=self.num_bits,
            signed=True
        )

    def to_unsigned(self):
        bits = copy.deepcopy(self.bits)
        return self.__class__(
            num=bits, num_bits=self.num_bits,
            signed=False
        )

    def __lshift__(self, bits):
        new_val = self.value << bits
        return self.__class__(
            num=new_val, num_bits=self.num_bits,
            signed=self.signed
        )

    def __rshift__(self, bits):
        new_val = self.value >> bits
        return self.__class__(
            num=new_val, num_bits=self.num_bits,
            signed=self.signed
        )

    @classmethod
    def from_bits(cls, bits, num_bits=32):
        pass

    def invert_index(self, index):
        return self.num_bits - index - 1

    def __len__(self):
        return len(self.bits)

    def __getitem__(self, index):
        if type(index) is int:
            assert index >= 0
            return self.bits[self.invert_index(index)]
        else:
            start_index = index.stop
            end_index = index.start + 1
            bits = self.bits[::-1][start_index:end_index][::-1]
            return self.__class__(
                num=bits, num_bits=len(bits),
                signed=self.signed
            )

    def __setitem__(self, index, bit_value: int):
        assert self.editable

        if type(index) is int:
            assert index >= 0
            assert bit_value in (0, 1)
            bit_index = self.invert_index(index)
            self.bits[bit_index] = bit_value
        else:
            if isinstance(bit_value, BinNumber):
                bit_value = bit_value.unsigned_value
                assert bit_value >= 0

            end_index = index.start
            start_index = index.stop - 1
            num_assign_bits = end_index - start_index

            assign_bits = self.fill_bits(
                bit_value, num_bits=num_assign_bits,
                negative=False
            )

            # print(start_index, end_index)
            start = self.invert_index(end_index)
            for k in range(num_assign_bits):
                self.bits[start+k] = assign_bits[k]

    @property
    def is_negative(self):
        return self.bits[0] == 1

    @property
    def is_positive(self):
        return not self.is_negative

    def to_bin(self, header='0b'):
        return header + ''.join([str(bit) for bit in self.bits])

    def to_decimal(self, bits=None, signed=None):
        if signed is None:
            signed = self.signed

        number = 0
        if bits is None:
            bits = self.bits

        bits = copy.deepcopy(bits)[::-1]

        for k, bit in enumerate(bits):
            bit_val = bit * 2 ** k
            if signed and (k == len(bits) - 1):
                bit_val *= -1

            number += bit_val

        return number

    @property
    def value(self):
        return self.to_decimal()

    @property
    def unsigned_value(self):
        return self.to_decimal(signed=False)

    @property
    def msb(self):
        return self.bits[0]

    def sign_extend(self, num_bits):
        assert num_bits >= self.num_bits
        padding = [self.msb] * (num_bits - self.num_bits)
        new_bits = padding + self.bits

        return self.__class__(
            num=copy.copy(new_bits),
            num_bits=num_bits, signed=self.signed
        )

    def editable_copy(self):
        return self.copy(editable=True)

    def copy(self, editable=False):
        for bit in self.bits:
            assert bit in (0, 1)

        return self.__class__(
            num=copy.copy(self.bits),
            num_bits=self.num_bits, signed=self.signed,
            editable=editable
        )

    def __add__(self, other):
        if isinstance(other, self.__class__):
            other = other.value

        new_val = self.value + other
        # print('add val', self, self.value, other, new_val)
        new_bin_no = self.__class__(
            num=new_val, num_bits=self.num_bits,
            signed=self.signed
        )

        try:
            assert (
                new_bin_no.value ==
                (new_val % (2 ** self.num_bits))
            )
        except AssertionError as e:
            print('VAL_MISMATCH', new_bin_no.value, new_val)
            raise e

        return new_bin_no

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            other = other.value

        new_val = self.value - other
        if not self.signed:
            new_val += 2 ** self.num_bits

        # print('new val', new_val)
        return self.__class__(
            num=new_val, num_bits=self.num_bits,
            signed=self.signed
        )

    def __mul__(self, other):
        value = self.value * other.value
        return self.__class__(
            num=value, num_bits=self.num_bits,
            signed=self.signed
        )

    def __truediv__(self, other):
        return self // other

    def __floordiv__(self, other):
        value = self.value // other.value
        return self.__class__(
            num=value, num_bits=self.num_bits,
            signed=self.signed
        )

    def __mod__(self, other):
        value = self.value % other.value
        return self.__class__(
            num=value, num_bits=self.num_bits,
            signed=self.signed
        )

    def __invert__(self):
        bits = copy.deepcopy(self.bits)
        print('old bits', bits)
        for k in range(len(bits)):
            bits[k] = 1 - bits[k]

        # print('new bits', bits)
        value = self.to_decimal(bits)
        inv_bin_no = self.__class__(
            num=value, num_bits=self.num_bits,
            signed=self.signed
        )

        print(f'inv_value', value, inv_bin_no)
        return inv_bin_no

    def __and__(self, other):
        assert self.num_bits == other.num_bits
        l_bits = copy.deepcopy(self.bits)
        r_bits = copy.deepcopy(other.bits)

        for k in range(len(l_bits)):
            l_bits[k] &= r_bits[k]

        return self.__class__(
            num=l_bits, num_bits=self.num_bits,
            signed=self.signed
        )

    def __or__(self, other):
        assert self.num_bits == other.num_bits
        l_bits = copy.deepcopy(self.bits)
        r_bits = copy.deepcopy(other.bits)

        for k in range(len(l_bits)):
            l_bits[k] |= r_bits[k]

        return self.__class__(
            num=l_bits, num_bits=self.num_bits,
            signed=self.signed
        )

    def __xor__(self, other):
        assert self.num_bits == other.num_bits
        l_bits = copy.deepcopy(self.bits)
        r_bits = copy.deepcopy(other.bits)

        for k in range(len(l_bits)):
            l_bits[k] ^= r_bits[k]

        return self.__class__(
            num=l_bits, num_bits=self.num_bits,
            signed=self.signed
        )

    def __neg__(self):
        return ~self + 1

    @staticmethod
    def fill_bits(num, num_bits=32, negative=False):
        str_num = bin(num)
        bits = [0] * num_bits

        for k, digit in enumerate(str_num[::-1]):
            if digit == 'b':
                break

            digit = 1 if digit == '1' else 0
            try:
                bits[-1-k] = digit
            except IndexError as e:
                break

        if negative:
            assert bits[0] == 0
            bits[0] = 1

        return bits

    def __bool__(self):
        return self.value != 0

    def __eq__(self, other):
        if isinstance(other, BinNumber):
            return self.value == other.value

        return self.value == other

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    @property
    def is_zero(self):
        return sum(self.bits) == 0

    def to_hex(self, num=None):
        if num is None:
            num = self.to_decimal(signed=False)

        str_num = hex(num)[2:]
        length = math.ceil(self.num_bits / 4)
        padded_hex = '0x' + str_num.zfill(length)
        return padded_hex

    def __repr__(self):
        name = self.__class__.__name__
        num = self.to_decimal()
        return (
            f'{name}({num}, '
            f'num_bits={self.num_bits}, '
            f'hex_val={self.to_hex()}'
            ')'
        )


if __name__ == '__main__':
    an = BinNumber(0)
    bn = BinNumber(0x55555555)
    cn = BinNumber(0x80000000)
    print(an, bn, cn)
    print(bn.to_bin())

    print('inv', ~bn)
    # print('inv inv', ~~bn)
    print('negative', -bn)
    print('SUB', an-bn)