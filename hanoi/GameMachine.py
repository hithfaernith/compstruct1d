from enum import IntEnum, auto
from overrides import overrides

from BitNumber import *
from ALU import ALU, ALUFN


class REGS(IntEnum):
    @overrides
    def _generate_next_value_(self, _start, count, _last_values):
        # Generate consecutive automatic numbers starting from zero
        return count

    PLAYER_POS = auto()
    LEVEL_NO = auto()

    ENEMY_NO = auto()
    ENEMY_POS = auto()
    ENEMY_DIR = auto()
    TOWER_NO = auto()
    TOWER = auto()

    ENEMY_POSITIONS = auto()
    ENEMY_DIRECTIONS = auto()
    TOWER_POSITIONS = auto()


class STATES(IntEnum):
    @overrides
    def _generate_next_value_(self, _start, count, _last_values):
        # Generate consecutive automatic numbers starting from zero
        return count

    START_STATE = auto()


class StateTransition(object):
    def __init__(
        self, a_sel, b_sel, a_const, b_const,
        alufn, we, wsel
    ):
        self.a_sel = a_sel
        self.b_sel = b_sel
        self.a_const = a_const
        self.b_const = b_const
        self.alufn = alufn

        self.we = we
        self.wsel = wsel


class GameMachine(object):
    CLOCK_FREQ = 1e9
    NUM_ENEMIES = 8
    NUM_DISKS = 4
    NUM_TOWERS = 3

    def __init__(self, clock_div=17):
        self.clock_div = clock_div
        self.registers = self.reset_registers()

    def reset_registers(self):
        self.registers = self.init_registers()
        return self.registers

    @property
    def enemy_no(self):
        return self.registers[REGS.ENEMY_NO]

    @property
    def enemy_positions(self):
        return self.registers[REGS.ENEMY_POSITIONS]

    @property
    def enemy_directions(self):
        return self.registers[REGS.ENEMY_DIRECTIONS]

    @property
    def enemy_pos(self):
        return self.enemy_positions[int(self.enemy_no)]

    @property
    def enemy_dir(self):
        return self.enemy_directions[int(self.enemy_no)]

    def init_registers(self):
        return {
            REGS.PLAYER_POS: UBitNumber(0, num_bits=8),
            REGS.ENEMY_NO: UBitNumber(0, num_bits=16),
            REGS.TOWER_NO: UBitNumber(0, num_bits=16),
            REGS.ENEMY_POSITIONS: {
                # y coordinate is k, x coord is 31 (right)
                k: UBitNumber(31 + k << 5, num_bits=8)
                for k in range(self.NUM_ENEMIES)
            }, REGS.ENEMY_DIRECTIONS: {
                k: UBitNumber(0b10, num_bits=2)
                for k in range(self.NUM_ENEMIES)
            }, REGS.TOWER_POSITIONS: {
                0: UBitNumber(7 << 5, num_bits=16),
                1: UBitNumber(15 << 5, num_bits=16),
                2: UBitNumber(22 << 5, num_bits=16)
            }
        }

    def run(self):
        raise NotImplementedError

