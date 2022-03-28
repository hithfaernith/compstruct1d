import copy
from enum import IntEnum

from BitNumber import *
from BitNumber import UBitNumber


class ALUFN(IntEnum):
    ADD = 0x00
    SUB = 0x01
    MUL = 0x02
    AND = 0x18
    OR = 0x1E
    XOR = 0x16
    A = 0x1A
    SHL = 0x20
    SHR = 0x21
    SRA = 0x23
    CMPEQ = 0x33
    CMPLT = 0x35
    CMPLE = 0x37


class ALU(object):
    BUS_WIDTH = 16
    ALUFN_WIDTH = 6

    @classmethod
    def verify(
        cls, a: UBitNumber, b: UBitNumber, alufn: UBitNumber
    ):
        try:
            assert isinstance(a, UBitNumber)
            assert isinstance(b, UBitNumber)
            assert isinstance(alufn, UBitNumber)

            assert not a.editable
            assert not b.editable
            assert a.num_bits == b.num_bits == cls.BUS_WIDTH
            assert alufn.num_bits == 6
        except AssertionError as e:
            print('VERIFY FAILED', a, b, alufn)
            raise e

    @classmethod
    def shift_unit(
        cls, a: UBitNumber, b: UBitNumber, alufn: UBitNumber
    ):
        cls.verify(a, b, alufn)
        shift_bits = b[3:0]
        shift_type = alufn[2:0]

        LEFT_SHIFT = 0b0
        RIGHT_SHIFT = 0b1
        LEFT_ARITH_SHIFT = 0b10
        RIGHT_ARITH_SHIFT = 0b11
        LEFT_ROTATE = 0b100
        RIGHT_ROTATE = 0b101

        if shift_type == LEFT_SHIFT:
            return a << shift_bits
        elif shift_type == RIGHT_SHIFT:
            return a >> shift_bits
        elif shift_type == LEFT_ARITH_SHIFT:
            return a.shift_left_arith(shift_bits)
        elif shift_type == RIGHT_ARITH_SHIFT:
            return a.shift_right_arith(shift_bits)
        elif shift_type == LEFT_ROTATE:
            return (a << bits) | (a >> (16 - bits))
        elif shift_type == RIGHT_ROTATE:
            return (a >> bits) | (a << (16 - bits))
        else:
            return a.copy()

    @classmethod
    def boolean_unit(
        cls, a: UBitNumber, b: UBitNumber, alufn: UBitNumber
    ):
        # print('BOOL UNIT')
        cls.verify(a, b, alufn)
        length = len(a)
        output = UBitNumber(0, num_bits=length, editable=True)
        func = alufn[3:0]

        for k in range(len(output)):
            lookup_index = a[k] + 2 * b[k]
            output[k] = func[lookup_index]
            # print('FUNC', k, func, lookup_index, func[lookup_index], a[k])

        output.disable_edit()
        return output

    @classmethod
    def compare_unit(
        cls, a: UBitNumber, b: UBitNumber, alufn: UBitNumber
    ):
        cls.verify(a, b, alufn)

        length = len(a)
        compare_code = alufn[2:1]
        output = UBitNumber(0, num_bits=length, editable=True)

        if compare_code == 0b01:
            output[0] = 1 if (a == b) else 0
        elif compare_code == 0b10:
            output[0] = 1 if (a < b) else 0
        elif compare_code == 0b11:
            output[0] = 1 if (a <= b) else 0

        output.disable_edit()
        return output

    @classmethod
    def run(cls, a: UBitNumber, b: UBitNumber, alufn: UBitNumber):
        if type(a) is int:
            a = UBitNumber(a, num_bits=cls.BUS_WIDTH)
        if type(b) is int:
            b = UBitNumber(b, num_bits=cls.BUS_WIDTH)

        if type(alufn) is int:
            alufn = UBitNumber(alufn, num_bits=cls.ALUFN_WIDTH)
        elif isinstance(alufn, IntEnum):
            alufn = UBitNumber(int(alufn), num_bits=cls.ALUFN_WIDTH)

        cls.verify(a, b, alufn)

        if alufn[5:1] == 0:
            return a + b
        elif alufn[5:0] == 0b000010:
            return a * b
        elif alufn[5:0] == 0b000011:
            return a // b
        elif alufn[5:3] == 0b001:
            raise NotImplementedError('REVERSE NOT IMPLEMENTED')
        elif alufn[5:4] == 0b01:
            return cls.boolean_unit(a, b, alufn)
        elif alufn[5:4] == 0b10:
            return cls.shift_unit(a, b, alufn)
        else:
            output = UBitNumber(0, num_bits=length)
            return output
