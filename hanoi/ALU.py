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
    def PLAYER_CLIP_MOVE(cls, a: UBitNumber, b: UBitNumber):
        # UP=0, DOWN=1, LEFT=2, RIGHT=3
        player_position = a
        new_position = UBitNumber(0, num_bits=16)
        # var player_move = b should work
        player_move = b.editable_copy()

        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

        y = player_position[7:5]
        x = player_position[4:0]

        if x == 0:
            # deny left [2] move
            player_move[LEFT] = 0
        elif x == 31:
            # deny right [3] move
            player_move[RIGHT] = 0

        if y == 0:
            # deny up [0] (visually down) move
            player_move[UP] = 0
        elif y == 31:
            # deny down [0] (visually up) move
            player_move[DOWN] = 0

        if player_move[UP] == 1:
            new_position

    @classmethod
    def math_unit(
        cls, a: UBitNumber, b: UBitNumber, alufn: UBitNumber
    ):
        cls.verify(a, b, alufn)
        assert alufn[5:4] == 0b00

        if alufn[3:0] == 0b0000:
            return a + b
        elif alufn[5:0] == 0b0010:
            return a * b
        elif alufn[5:0] == 0b0011:
            return a // b
        elif alufn[5:0] == 0b1000:
            return cls.PLAYER_CLIP_MOVE(a, b, alufn)

        raise

    @classmethod
    def run(cls, a: UBitNumber, b: UBitNumber, alufn: UBitNumber):
        # TODO: remove reverse ALUFN from lucid code
        if type(a) is int:
            a = UBitNumber(a, num_bits=cls.BUS_WIDTH)
        if type(b) is int:
            b = UBitNumber(b, num_bits=cls.BUS_WIDTH)

        if type(alufn) is int:
            alufn = UBitNumber(alufn, num_bits=cls.ALUFN_WIDTH)
        elif isinstance(alufn, IntEnum):
            alufn = UBitNumber(int(alufn), num_bits=cls.ALUFN_WIDTH)

        cls.verify(a, b, alufn)

        if alufn[5:4] == 0b00:
            return cls.math_unit(a, b, alufn)
        elif alufn[5:4] == 0b01:
            return cls.boolean_unit(a, b, alufn)
        elif alufn[5:4] == 0b10:
            return cls.shift_unit(a, b, alufn)
        elif alufn[5:4] == 0b11:
            return cls.compare_unit(a, b, alufn)
        else:
            output = UBitNumber(0, num_bits=length)
            return output
