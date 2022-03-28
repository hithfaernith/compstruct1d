from overrides import overrides
from BinNumber import BinNumber


class BitNumber(BinNumber):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        name = self.__class__.__name__
        num = self.to_bin()
        return (
            f'{name}({num}, num_bits={self.num_bits})'
        )

    def msb_index(self):
        for k in range(self.num_bits):
            if self.bits[k] == 1:
                return self.invert_index(k)

        return None

    def solo_msb(self):
        # take out all bits except the MSB
        # i.e. 0b01011 becomes 0b01000
        msb_index = self.msb_index()
        new_num = BitNumber(num=0, num_bits=self.num_bits)
        if msb_index is None:
            return new_num

        new_num[msb_index] = 1
        return new_num


class UnsignedBitNumber(BitNumber):
    def __init__(self, *args, **kwargs):
        kwargs['signed'] = False
        super().__init__(*args, **kwargs)

    @overrides
    def to_unsigned(self):
        return copy.deepcopy(self)

    @overrides
    def to_signed(self):
        bits = copy.deepcopy(self.bits)
        return SignedBitNumber(
            num=bits, num_bits=self.num_bits
        )


class UBitNumber(UnsignedBitNumber):
    pass


class UShort16(UBitNumber):
    def __init__(self, *args, num_bits=16, **kwargs):
        super().__init__(*args, num_bits=num_bits, **kwargs)


class SignedBitNumber(BitNumber):
    def __init__(self, *args, **kwargs):
        kwargs['signed'] = True
        super().__init__(*args, **kwargs)

    @overrides
    def to_signed(self):
        return copy.deepcopy(self)

    @overrides
    def to_unsigned(self):
        bits = copy.deepcopy(self.bits)
        return UnsignedBitNumber(
            num=bits, num_bits=self.num_bits
        )
