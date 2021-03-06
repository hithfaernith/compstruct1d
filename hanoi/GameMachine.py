import textwrap
from enum import Enum, IntEnum, auto

from BitNumber import *
from ALU import ALU, ALUFN


class REGS(IntEnum):
    """
    register names
    translate this to a global FSM in lucid
    """

    def _generate_next_value_(self, start, count, last_values):
        # Generate consecutive automatic numbers starting from zero
        return count

    PMOVE = auto()
    PLAYER_POS = auto()
    PLAYER_COUNTER = auto()
    LEVEL_NO = auto()

    ENEMY_NO = auto()
    TOWER_NO = auto()
    ACTIVE_DISK = auto()

    # multiplexed registers
    ENEMY_DIR = auto()
    ENEMY_POS = auto()
    ENEMY_MOVE_WAIT = auto()
    TOWER_POS = auto()
    TOWER = auto()

    ENEMY_POSITIONS = auto()
    ENEMY_MOVE_WAITS = auto()
    ENEMY_DIRECTIONS = auto()
    TOWER_POSITIONS = auto()
    TOWER_STATES = auto()

    LEVEL_DISKS = auto()
    LAST_FIRE_WAIT = auto()
    GAME_STATE = auto()
    GAME_LEVEL = auto()


class StateTransition(object):
    def __init__(
        self, we, wsel, next_state,
        alu_output, signal_render, soft_reset=False
    ):
        self.we = we
        self.wsel = wsel
        self.next_state = next_state
        self.alu_output = alu_output
        self.signal_render = signal_render
        self.soft_reset = soft_reset

    def __repr__(self):
        return self.__class__.__name__ + '(' + (
            f'we={self.we}, wsel={self.wsel}, '
            f'next_state={self.next_state}, '
            f'alu_output={self.alu_output},'
            f'signal_render={self.signal_render}'
            f')'
        )


class GameMachine(object):
    NUM_ENEMIES = 8
    NUM_DISKS = 4
    NUM_TOWERS = 3

    def __init__(self):
        self.registers = self.reset_registers()
        self.state = None
        self.cycles = None
        self.render_ready = False

        self.a_sel = None
        self.b_sel = None
        self.alufn = None

    def reset_state(self, reset_cycles=True):
        self.state = None
        self.render_ready = False
        self.reset_registers()

        if reset_cycles:
            self.cycles = 0

    def clear_render_flag(self):
        self.render_ready = False

    def reset_registers(self):
        self.registers = self.init_registers()
        return self.registers

    @property
    def player_pos(self):
        return self.registers[REGS.PLAYER_POS]

    @player_pos.setter
    def player_pos(self, value: UBitNumber):
        player_pos = self.registers[REGS.PLAYER_POS]
        player_pos.enable_edit()
        player_pos[7:0] = value
        player_pos.disable_edit()

    @property
    def level_disks(self):
        return self.registers[REGS.LEVEL_DISKS]

    @property
    def game_state(self):
        return self.registers[REGS.GAME_STATE]

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

    @enemy_pos.setter
    def enemy_pos(self, value: UBitNumber):
        assert isinstance(value, UBitNumber)
        self.enemy_positions[int(self.enemy_no)] = value[7:0]

    @property
    def enemy_dir(self):
        return self.enemy_directions[int(self.enemy_no)]

    @enemy_dir.setter
    def enemy_dir(self, value: UBitNumber):
        assert isinstance(value, UBitNumber)
        self.enemy_directions[int(self.enemy_no)] = value[1:0]

    @property
    def enemy_move_waits(self):
        return self.registers[REGS.ENEMY_MOVE_WAITS]

    @property
    def enemy_move_wait(self):
        return self.enemy_move_waits[int(self.enemy_no)]

    @enemy_move_wait.setter
    def enemy_move_wait(self, value: UBitNumber):
        assert isinstance(value, UBitNumber)
        assert value.num_bits == 16
        self.enemy_move_waits[int(self.enemy_no)] = value

    @property
    def tower_positions(self):
        return self.registers[REGS.TOWER_POSITIONS]

    @property
    def towers(self):
        return self.registers[REGS.TOWER]

    @property
    def tower_states(self):
        return self.registers[REGS.TOWER_STATES]

    @property
    def tower_no(self):
        return self.registers[REGS.TOWER_NO]

    @tower_no.setter
    def tower_no(self, value: UBitNumber):
        assert isinstance(value, UBitNumber)
        assert value.num_bits == 16
        self.registers[REGS.TOWER_NO] = value

    @property
    def tower_state(self):
        return self.tower_states[int(self.tower_no)]

    @tower_state.setter
    def tower_state(self, value: UBitNumber):
        assert isinstance(value, UBitNumber)
        self.tower_states[int(self.tower_no)] = value[3:0]

    @property
    def tower_pos(self):
        return self.tower_positions[int(self.tower_no)]

    @tower_pos.setter
    def tower_pos(self, value: UBitNumber):
        assert isinstance(value, UBitNumber)
        self.tower_positions[int(self.tower_no)] = value[7:0]

    @property
    def active_disk(self):
        return self.registers[REGS.ACTIVE_DISK]

    @property
    def game_level(self):
        return self.registers[REGS.GAME_LEVEL]

    def init_registers(self):
        # intiialize all used registers with their starting values

        return {
            REGS.PLAYER_POS: UBitNumber(0, num_bits=8),
            REGS.PLAYER_COUNTER: UBitNumber(0, num_bits=16),
            REGS.ENEMY_NO: UBitNumber(0, num_bits=16),
            REGS.TOWER_NO: UBitNumber(0, num_bits=16),
            # how long it's been since the last enemy was fired
            REGS.LAST_FIRE_WAIT: UBitNumber(0, num_bits=16),
            REGS.ACTIVE_DISK: UBitNumber(0b0000, num_bits=4),
            # whether game is ongoing(00), lost(01) or won(10)
            REGS.GAME_STATE: UBitNumber(0b00, num_bits=2),

            # game level no. (0, 1, 2, 3)
            REGS.GAME_LEVEL: UBitNumber(0b00, num_bits=2),
            # disks on the first tower at the start if each level
            REGS.LEVEL_DISKS: UBitNumber(0b1000, num_bits=4),

            REGS.ENEMY_POSITIONS: {
                # y coordinate is k, x coord is 31 (right)
                k: UBitNumber(31 + (k << 5), num_bits=8)
                for k in range(self.NUM_ENEMIES)
            }, REGS.ENEMY_DIRECTIONS: {
                k: UBitNumber(0b00, num_bits=2)
                for k in range(self.NUM_ENEMIES)
            }, REGS.ENEMY_MOVE_WAITS: {
                # how long since the enemy last moved
                k: UBitNumber(0b0, num_bits=16)
                for k in range(self.NUM_ENEMIES)
            }, REGS.TOWER_POSITIONS: {
                0: UBitNumber((4 << 5) + 7, num_bits=8),
                1: UBitNumber((6 << 5) + 15, num_bits=8),
                2: UBitNumber((5 << 5) + 22, num_bits=8)
            }, REGS.TOWER_STATES: {
                0: UBitNumber(0b1000, num_bits=4),
                1: UBitNumber(0, num_bits=4),
                2: UBitNumber(0, num_bits=4)
            }
        }

    def soft_reset(self):
        self.write_register(
            REGS.PLAYER_POS, UBitNumber(0, num_bits=16)
        )
        self.write_register(
            REGS.ACTIVE_DISK, UBitNumber(0, num_bits=4)
        )

        for k in range(self.NUM_ENEMIES):
            self.registers[REGS.ENEMY_DIRECTIONS][k] = UBitNumber(
                0, num_bits=8
            )
        for k in range(3):
            self.registers[REGS.TOWER_STATES][k] = UBitNumber(
                0, num_bits=4
            )

        tower = UBitNumber(0b1000, num_bits=4)
        if self.game_level == 0:
            tower = UBitNumber(0b1000, num_bits=4)
        elif self.game_level == 1:
            tower = UBitNumber(0b1100, num_bits=4)
        elif self.game_level == 2:
            tower = UBitNumber(0b1110, num_bits=4)
        elif self.game_level == 3:
            tower = UBitNumber(0b1111, num_bits=4)

        # set disks that end tower should have to finish level
        self.write_register(REGS.LEVEL_DISKS, tower)
        self.registers[REGS.TOWER_STATES][0] = tower
        # will be seen and replaced with STATES.START
        # in state_transition
        self.state = None

    def read(self, register):
        if register == REGS.ENEMY_DIR:
            return self.enemy_dir
        elif register == REGS.ENEMY_POS:
            return self.enemy_pos
        elif register == REGS.TOWER_POS:
            return self.tower_pos
        elif register == REGS.TOWER:
            return self.tower_state
        elif register == REGS.ENEMY_MOVE_WAIT:
            return self.enemy_move_wait

        result = self.registers[register]
        assert isinstance(result, UBitNumber)
        return result

    def write_register(self, register, value):
        if register == REGS.ENEMY_DIR:
            self.enemy_dir = value
        elif register == REGS.ENEMY_POS:
            self.enemy_pos = value
        elif register == REGS.PLAYER_POS:
            self.player_pos = value
        elif register == REGS.TOWER_POS:
            self.tower_pos = value
        elif register == REGS.TOWER:
            self.tower_state = value
        elif register == REGS.ENEMY_MOVE_WAIT:
            self.enemy_move_wait = value
        else:
            assert isinstance(value, UBitNumber)
            assert isinstance(self.registers[register], UBitNumber)
            reg_bits = self.registers[register].num_bits
            value = value[reg_bits-1:0]

            try:
                assert reg_bits == value.num_bits
            except AssertionError as e:
                print(f'REG FAIL {register} {value} {value.num_bits} {reg_bits}')
                print(REGS(register))
                raise e

            self.registers[register].enable_edit()
            self.registers[register][reg_bits-1:0] = value
            self.registers[register].disable_edit()

    def run_alu(self, a_sel, b_sel, alufn):
        a, b = a_sel, b_sel

        if isinstance(a, Enum):
            a = self.read(a_sel)
            assert isinstance(a, UBitNumber)
        elif type(a) is int:
            a = UBitNumber(a, num_bits=16)

        if isinstance(b, Enum):
            b = self.read(b_sel)
            assert isinstance(b, UBitNumber)
        elif type(b) is int:
            b = UBitNumber(b, num_bits=16)

        if isinstance(alufn, IntEnum):
            alufn = UBitNumber(int(alufn), num_bits=6)

        try:
            assert isinstance(a, UBitNumber)
            assert isinstance(b, UBitNumber)
        except AssertionError as e:
            print(f'BAD A,B = {a,b}')
            print(isinstance(a, Enum), isinstance(b, Enum))
            print(isinstance(a, UBitNumber), isinstance(b, UBitNumber))
            raise e

        # TODO: ensure we do unsigned extend in lucid also
        a_sext = a.unsigned_extend(num_bits=16)
        b_sext = b.unsigned_extend(num_bits=16)
        result = ALU.run(a_sext, b_sext, alufn)
        return result

    @property
    def alu_output(self):
        return self.run_alu(
            self.a_sel, self.b_sel, self.alufn
        )

    def step(self, PMOVE, PICK_OR_DROP=None):
        state_transition = self.state_transition(PMOVE, PICK_OR_DROP)
        try:
            self.apply_transition(state_transition)
        except Exception as e:
            print('STATE TRANSITION', state_transition)
            raise e

    def apply_transition(self, state_transition):
        if state_transition.we:
            self.write_register(
                register=state_transition.wsel,
                value=state_transition.alu_output
            )

        if state_transition.soft_reset:
            self.soft_reset()

        assert isinstance(state_transition.next_state, Enum)
        self.state = state_transition.next_state
        # print(state_transition.signal_render)
        self.render_ready |= state_transition.signal_render
        self.cycles += 1

    def state_transition(
        self, PMOVE: UBitNumber, PICK_OR_DROP: UBitNumber = None
    ):
        """
        simple(r) state transition rules for
        just moving the player around the map
        """

        class STATES(IntEnum):
            START = auto()
            PLAYER_INIT = auto()
            INC_PLAYER_POS = auto()
            CMP_PLAYER_WAIT = auto()
            PLAYER_MOVE = auto()

        _PLAYER_WAIT = 70
        state_init = False

        if self.state is None:
            state_init = True
            self.state = STATES.START

        we, wsel = None, None
        next_state, signal_render = None, True

        if self.state == STATES.START:
            self.a_sel = PMOVE  # ACONST = 0
            self.b_sel = 0x0000  # BCONST = 1
            self.alufn = ALUFN.CMPEQ

            we, wsel = 0, 0
            next_state = STATES.PLAYER_INIT

        elif self.state == STATES.PLAYER_INIT:
            self.a_sel = 0x0000
            self.b_sel = 0x0000
            self.alufn = ALUFN.A

            we, wsel = 1, REGS.PLAYER_COUNTER
            next_state = STATES.INC_PLAYER_POS

        elif self.state == STATES.INC_PLAYER_POS:
            self.a_sel = REGS.PLAYER_COUNTER
            self.b_sel = 0x0001
            self.alufn = ALUFN.ADD

            we, wsel = 1, REGS.PLAYER_COUNTER
            next_state = STATES.CMP_PLAYER_WAIT

        elif self.state == STATES.CMP_PLAYER_WAIT:
            self.a_sel = REGS.PLAYER_COUNTER
            self.b_sel = _PLAYER_WAIT  # BCONST = 1
            self.alufn = ALUFN.CMPLT

            we, wsel = 0, 0
            # I'm using a @property to instantaneously
            # propagate self.a_sel, self.b_sel to self.alu_output
            if self.alu_output:
                next_state = STATES.INC_PLAYER_POS
            else:
                next_state = STATES.PLAYER_MOVE

        elif self.state == STATES.PLAYER_MOVE:
            self.a_sel = REGS.PLAYER_POS
            self.b_sel = PMOVE
            self.alufn = ALUFN.PLAYER_CLIP_MOVE

            we, wsel = 1, REGS.PLAYER_POS
            next_state = STATES.PLAYER_INIT

        else:
            raise ValueError(f'INVALID STATE {self.state}')

        assert we is not None
        assert wsel is not None
        assert next_state is not None

        assert next_state in STATES
        return StateTransition(
            we=we, wsel=wsel, alu_output=self.alu_output,
            next_state=next_state, signal_render=signal_render
        )
