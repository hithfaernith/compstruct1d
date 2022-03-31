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

        _PLAYER_WAIT = 40
        state_init = False

        if self.state is None:
            state_init = True
            self.state = STATES.START

        we, wsel = None, None
        next_state = None

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
            next_state=next_state
        )