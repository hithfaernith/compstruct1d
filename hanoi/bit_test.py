from BitNumber import *
from ALU import ALU, ALUFN
from enum import IntEnum

a = BitNumber(num=0b1101101011)
print(a, a[5:0], a[5:0].value, a[5:1])
# verify lucid / jsim-style indexing
print(a[0], a[1], a[2])

b = BitNumber(-1, num_bits=3)
c = BitNumber(0b111, num_bits=3)
print(b, c, b == c)

d = UnsignedBitNumber(0b111, num_bits=3)
e = SignedBitNumber(0b111, num_bits=3)
print(d, e, d.value, e.value, d == e, d == 7)

a = UBitNumber(16, num_bits=8)
b = UBitNumber(3, num_bits=4)
print('DIVIDE', a, b, a // b)
print(b, b << 3, b << 2)

print(int(ALUFN.A), type(ALUFN.A), isinstance(ALUFN.A, IntEnum))
print(ALU.run(6, 1, ALUFN.A))

a = UBitNumber(0b10111001, num_bits=8)
b = UBitNumber(23, num_bits=8)
print(a, a.sign_extend(16), b, b.sign_extend(16))

print(b)
b += 1
print(b)

a = UBitNumber(0, num_bits=8).enable_edit()
a[4:1] = 0b1011
print(a, a + 1)

a = UBitNumber(0, num_bits=8).enable_edit()
print(a, a - 1)