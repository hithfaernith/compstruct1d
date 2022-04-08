from BitNumber import UBitNumber


def split_instruction(instr_hex):
    instr = UBitNumber(instr_hex, num_bits=32)
    opcode = instr[31:26]
    rc = instr[25:21]
    ra = instr[20:16]
    literal = instr[15:0]

    print(f'opcode = {opcode}')
    print(f'rc = {rc}')
    print(f'ra = {ra}')
    print(f'literal = {literal}')


if __name__ == '__main__':
    """
    ADDC(R1,128,R7): 0xC0E10080
    LD(R11,-4,R0): 0x600BFFFC
    ST(R0,-4,R11): 0x640BFFFC
    BEQ(R9,0x1C,R27): 0x77690002
    """
    print('ADDC(R1,128,R7): 0xC0E10080')
    split_instruction(0xC0E10080)
    print('\nLD(R11,-4,R0): 0x600BFFFC')
    split_instruction(0x600BFFFC)
    print('\nST(R0,-4,R11): 0x640BFFFC')
    split_instruction(0x640BFFFC)
    print('\nBEQ(R9,0x1C,R27): 0x77690002')
    split_instruction(0x77690002)