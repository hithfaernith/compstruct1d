from BitNumber import *
from GameMachine import *

from ALU import ALU, ALUFN
from enum import Enum, IntEnum, auto


class HanoiMachine(GameMachine):
    def state_transition(self, PMOVE: UBitNumber):
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

            INIT_ENEMY_POS = auto()
            INIT_ENEMY_NO = auto()
            INC_ENEMY_NO = auto()
            CHECK_ENEMY_NO = auto()
            IF_ENEMY_HIDDEN = auto()
            LAST_FIRE_CHECK = auto()
            INC_FIRE_WAIT = auto()
            ENEMY_WAIT_CHECK = auto()
            INC_ENEMY_WAIT = auto()
            RESET_ENEMY_WAIT = auto()
            FIRE_ENEMY = auto()
            RESET_FIRE_WAIT = auto()
            SET_ENEMY_POS = auto()
            CHECK_ENEMY_LEFT = auto()
            ENEMY_MOVE_LEFT = auto()
            ENEMY_HIDE = auto()
            COLLISION_CHECK = auto()

            DEATH = auto()

            RESET_TOWER_NO = auto()
            INC_TOWER_NO = auto()
            TOWER_NO_CMP = auto()
            CHECK_TOWER_POS = auto()
            IF_DROPPABLE = auto()
            DROP_DISK = auto()
            CLEAR_DISK_SEL = auto()
            IF_PICKABLE = auto()
            PICK_DISK = auto()
            RM_TOWER_DISK = auto()

            WIN_CHECK = auto()
            WIN = auto()

        _PLAYER_WAIT = 6
        _ENEMY_MOVE_DELAY = 2
        _MIN_FIRE_DELAY = 70
        state_init = False

        if self.state is None:
            state_init = True
            self.state = STATES.START

        we, wsel = None, None
        next_state, signal_render = None, False

        if self.state == STATES.START:
            self.a_sel = PMOVE  # ACONST = 0
            self.b_sel = 0x0000  # BCONST = 1
            self.alufn = ALUFN.CMPEQ
            signal_render = True

            we, wsel = 0, 0
            if self.alu_output:
                next_state = STATES.START
            else:
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
            signal_render = True

        elif self.state == STATES.CMP_PLAYER_WAIT:
            self.a_sel = REGS.PLAYER_COUNTER
            self.b_sel = _PLAYER_WAIT  # BCONST = 1
            self.alufn = ALUFN.CMPLT

            we, wsel = 0, 0
            # I'm using a @property to instantaneously
            # propagate self.a_sel, self.b_sel to self.alu_output
            if self.alu_output:
                next_state = STATES.INIT_ENEMY_NO
            else:
                next_state = STATES.PLAYER_MOVE

        elif self.state == STATES.PLAYER_MOVE:
            self.a_sel = REGS.PLAYER_POS
            self.b_sel = PMOVE
            self.alufn = ALUFN.PLAYER_CLIP_MOVE

            we, wsel = 1, REGS.PLAYER_POS
            next_state = STATES.PLAYER_INIT

        elif self.state == STATES.INIT_ENEMY_NO:
            self.a_sel = 0
            self.b_sel = 1
            self.alufn = ALUFN.SUB

            we, wsel = 1, REGS.ENEMY_NO
            next_state = STATES.INC_ENEMY_NO

        elif self.state == STATES.INC_ENEMY_NO:
            self.a_sel = REGS.ENEMY_NO
            self.b_sel = 0b1
            self.alufn = ALUFN.ADD

            we, wsel = 1, REGS.ENEMY_NO
            next_state = STATES.CHECK_ENEMY_NO

        elif self.state == STATES.CHECK_ENEMY_NO:
            self.a_sel = REGS.ENEMY_NO
            self.b_sel = 7
            self.alufn = ALUFN.CMPLT

            we, wsel = 0, 0
            b_sel = self.enemy_no
            # print(f'IF ENEM NO', self.a_sel, b_sel, self.alu_output)

            if self.alu_output:
                # less than is true
                next_state = STATES.IF_ENEMY_HIDDEN
            else:
                # TODO: tie to tower update FSM
                next_state = STATES.INC_PLAYER_POS

        elif self.state == STATES.IF_ENEMY_HIDDEN:
            self.a_sel = REGS.ENEMY_DIR
            self.b_sel = 0x00
            self.alufn = ALUFN.CMPEQ

            we, wsel = 0, 0
            if self.alu_output:
                next_state = STATES.LAST_FIRE_CHECK
            else:
                next_state = STATES.ENEMY_WAIT_CHECK

        elif self.state == STATES.ENEMY_WAIT_CHECK:
            self.a_sel = REGS.ENEMY_MOVE_WAIT
            self.b_sel = _ENEMY_MOVE_DELAY
            self.alufn = ALUFN.CMPLT

            we, wsel = 0, 0
            if self.alu_output:
                # less than is true
                next_state = STATES.INC_ENEMY_WAIT
            else:
                next_state = STATES.RESET_ENEMY_WAIT

        elif self.state == STATES.LAST_FIRE_CHECK:
            self.a_sel = REGS.LAST_FIRE_WAIT
            self.b_sel = _MIN_FIRE_DELAY
            self.alufn = ALUFN.CMPLT

            we, wsel = 0, 0
            if self.alu_output:
                # less than is true
                next_state = STATES.INC_FIRE_WAIT
            else:
                next_state = STATES.FIRE_ENEMY

        elif self.state == STATES.INC_FIRE_WAIT:
            self.a_sel = REGS.LAST_FIRE_WAIT
            self.b_sel = 1
            self.alufn = ALUFN.ADD

            # print('WAIT', self.registers[REGS.LAST_FIRE_WAIT])
            we, wsel = 1, REGS.LAST_FIRE_WAIT
            next_state = STATES.INC_ENEMY_NO

        elif self.state == STATES.FIRE_ENEMY:
            self.a_sel = 0b10
            self.b_sel = 0b0
            self.alufn = ALUFN.A

            we, wsel = 1, REGS.ENEMY_DIR
            next_state = STATES.SET_ENEMY_POS

        elif self.state == STATES.SET_ENEMY_POS:
            self.a_sel = 0x1F
            self.b_sel = REGS.PLAYER_POS
            self.alufn = ALUFN.OR

            we, wsel = 1, REGS.ENEMY_POS
            next_state = STATES.RESET_FIRE_WAIT
            # print(self.a_sel, self.player_pos, self.alu_output)

        elif self.state == STATES.RESET_FIRE_WAIT:
            self.a_sel = 0
            self.b_sel = 0
            self.alufn = ALUFN.A

            we, wsel = 1, REGS.LAST_FIRE_WAIT
            next_state = STATES.INC_ENEMY_NO

        elif self.state == STATES.INC_ENEMY_WAIT:
            # too soon since enemy last moved
            self.a_sel = REGS.ENEMY_MOVE_WAIT
            self.b_sel = 1
            self.alufn = ALUFN.ADD

            we, wsel = 1, REGS.ENEMY_MOVE_WAIT
            next_state = STATES.COLLISION_CHECK

        elif self.state == STATES.RESET_ENEMY_WAIT:
            self.a_sel = 0
            self.b_sel = 0
            self.alufn = ALUFN.A

            we, wsel = 1, REGS.ENEMY_MOVE_WAIT
            next_state = STATES.CHECK_ENEMY_LEFT

        elif self.state == STATES.CHECK_ENEMY_LEFT:
            self.a_sel = REGS.ENEMY_POS
            self.b_sel = 0x1F
            self.alufn = ALUFN.AND

            we, wsel = 0, 0
            if self.alu_output:
                # if alu_output is not zero
                next_state = STATES.ENEMY_MOVE_LEFT
            else:
                next_state = STATES.ENEMY_HIDE

        elif self.state == STATES.ENEMY_HIDE:
            self.a_sel = 0
            self.b_sel = 0
            self.alufn = ALUFN.A

            we, wsel = 1, REGS.ENEMY_DIR
            next_state = STATES.INC_ENEMY_NO

        elif self.state == STATES.ENEMY_MOVE_LEFT:
            self.a_sel = REGS.ENEMY_POS
            self.b_sel = 1
            self.alufn = ALUFN.ENEMY_MOVE_LEFT

            # print('MOVE LEFT')
            # print(self.enemy_pos, self.b_sel, self.alu_output)
            we, wsel = 1, REGS.ENEMY_POS
            next_state = STATES.COLLISION_CHECK

        elif self.state == STATES.COLLISION_CHECK:
            self.a_sel = REGS.ENEMY_POS
            self.b_sel = REGS.PLAYER_POS
            self.alufn = ALUFN.CMPEQ

            we, wsel = 0, 0
            if self.alu_output:
                next_state = STATES.DEATH
            else:
                next_state = STATES.INC_ENEMY_NO

        elif self.state == STATES.DEATH:
            self.a_sel = 0
            self.b_sel = 0
            self.alufn = ALUFN.CMPEQ

            we, wsel = 0, 0
            next_state = STATES.DEATH
            signal_render = True

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