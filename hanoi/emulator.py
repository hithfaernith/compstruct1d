import time

# Import and initialize the pygame library
import pygame

from enum import Enum, IntEnum
from timeit import default_timer as timer

from pygame.locals import *
from GameMachine import GameMachine
from HanoiMachine import HanoiMachine
from BitNumber import *

X_LEDS, Y_LEDS = 32, 8
X_BUFFER, Y_BUFFER = 128, 128
MAX_DISKS = 4
LED_SIZE = 32


class Colors(IntEnum):
    BLACK = 0x000000
    WHITE = 0xFFFFFF
    BLUE = 0x0000FF
    GREEN = 0x00FF00
    DARK_GREEN = 0x013220
    CELADON = 0xAFE1AF
    PURPLE = 0xDDA0DD
    INDIGO = 0x4B0082
    RED = 0xFF0000

    PLAYER = GREEN
    TOWER = BLUE
    ENEMY = RED
    DISK = INDIGO
    ACTIVE_DISK = DARK_GREEN


class Emulator(object):
    CLOCK_FREQ = 100 * 1e6  # 100 MHz clock

    def __init__(self, clock_div=16):
        self.clock_div = clock_div
        self.state = HanoiMachine()
        self.screen = None

    def init_screen(self):
        self.screen = pygame.display.set_mode([
            2 * X_BUFFER + X_LEDS * LED_SIZE,
            2 * Y_BUFFER + Y_LEDS * LED_SIZE
        ])

        return self.screen

    @staticmethod
    def disk_length(tower: UBitNumber, height=0):
        # print(MAX_DISKS)
        lengths = {k: 0 for k in range(MAX_DISKS)}
        assert len(lengths) == MAX_DISKS
        num_disks = 0

        for k in range(MAX_DISKS):
            if tower[k] == 1:
                lengths[num_disks] = MAX_DISKS - k
                num_disks += 1

        # print(lengths)
        return lengths[height]

    @staticmethod
    def max_disk_length(disk_selection: UBitNumber):
        for k in range(MAX_DISKS):
            if disk_selection[k] == 1:
                return MAX_DISKS - k

        return 0

    def fill_leds(self):
        num_pixels = X_LEDS * Y_LEDS
        pixel_colors = [
            [Colors.BLACK.value] * X_LEDS for _ in range(Y_LEDS)
        ]

        player_pos: UBitNumber = self.state.player_pos
        player_x, player_y = self.extract_position(player_pos)
        # set player color on led pixel buffer
        pixel_colors[player_y][player_x] |= Colors.PLAYER.value

        active_disk = self.state.active_disk
        active_disk_length = self.max_disk_length(active_disk)
        for k in range(active_disk_length):
            try:
                pixel_colors[player_y][player_x + k + 1] |= (
                    Colors.ACTIVE_DISK.value
                )
            except IndexError as e:
                break

        for tower_no in range(3):
            # set tower colors on led pixel buffer
            tower = self.state.tower_states[tower_no]
            tower_pos = self.state.tower_positions[tower_no]
            tower_x, tower_y = self.extract_position(tower_pos)

            for y in range(tower_y):
                pixel_colors[y][tower_x] |= Colors.TOWER.value

            for height in range(MAX_DISKS):
                disk_length = self.disk_length(tower, height)
                for k in range(disk_length):
                    pixel_colors[height][tower_x + k + 1] |= (
                        Colors.DISK.value
                    )

        for enemy_no in range(8):
            # draw enemy colors on led pixel buffer
            enemy_pos = self.state.enemy_positions[enemy_no]
            enemy_dir = self.state.enemy_directions[enemy_no]
            # enemies that aren't moving are considered invisible
            if enemy_dir == 0:
                continue

            enemy_x, enemy_y = self.extract_position(enemy_pos)
            pixel_colors[enemy_y][enemy_x] |= Colors.ENEMY.value

        for k in range(num_pixels):
            x, y, = k % X_LEDS, k // X_LEDS
            # we invert the y coordinate when actually
            # drawing the LED bec
            invert_y = (num_pixels // X_LEDS) - y - 1
            led_color = pixel_colors[y][x]

            pygame.draw.rect(self.screen, led_color, rect=(
                X_BUFFER + x * LED_SIZE,
                Y_BUFFER + invert_y * LED_SIZE,
                LED_SIZE - 1, LED_SIZE - 1
            ))

    @staticmethod
    def extract_position(bit_position: UBitNumber):
        # decode the 8 bit position register into x and y
        # integer coordinates respectively
        x, y = int(bit_position[4:0]), int(bit_position[7:5])
        return x, y

    @property
    def clocks_per_second(self):
        return self.CLOCK_FREQ / (2 ** self.clock_div)

    def logic_time_elapsed(self, cycles=None):
        """
        get amount of time that should've elapsed
        given the number of state transitions (game logic updates)
        that has occurred thus far. I want this to lock in the
        game FSM update rate independently of the display FPS
        """
        if cycles is None:
            cycles = self.state.cycles

        clocks_per_second = self.CLOCK_FREQ / (2 ** self.clock_div)
        logic_time_elapsed = cycles / clocks_per_second
        return logic_time_elapsed

    def run(self):
        pygame.init()
        self.state.reset_state()
        self.init_screen()
        running = True
        frames = 0

        start_time = timer()
        last_logic_lag = 0
        PMOVE = UBitNumber(0, num_bits=5)
        """
        io_button is simply the 5 push buttons. io_button[0] is up,
        io_button[1] is center, io_button[2] is down, io_button[3]
        is left, and io_button[4] is right.
        
        I've changed PMOVE[4:0] player input bit assignment to
        [PICK/DROP][4] [RIGHT][3] [LEFT][2] [DOWN][1] [UP][0]
        """

        while running:
            PMOVE.enable_edit()

            # PMOVE.zero_all_bits()
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        PMOVE[0] = 1  # up
                    elif event.key == pygame.K_s:
                        PMOVE[1] = 1  # down
                    elif event.key == pygame.K_a:
                        PMOVE[2] = 1  # left
                    elif event.key == pygame.K_d:
                        PMOVE[3] = 1  # right
                    elif event.key == pygame.K_SPACE:
                        PMOVE[4] = 1  # space

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        PMOVE[0] = 0  # up
                    elif event.key == pygame.K_s:
                        PMOVE[1] = 0  # down
                    elif event.key == pygame.K_a:
                        PMOVE[2] = 0  # left
                    elif event.key == pygame.K_d:
                        PMOVE[3] = 0  # right
                    elif event.key == pygame.K_SPACE:
                        PMOVE[4] = 0  # space

            # Fill the background with gray
            self.screen.fill((100, 100, 100))
            PMOVE.disable_edit()

            timestamp = timer()
            time_passed = timestamp - start_time
            logic_time_elapsed = self.logic_time_elapsed()
            lag = time_passed - logic_time_elapsed

            if (lag > 0.5) and (lag - last_logic_lag > 0.5):
                print('WARNING: GAME LOGIC UPDATE CANT KEEPUP')
                print(f'lag: {lag} {logic_time_elapsed}')
                last_logic_lag = lag
            else:
                last_logic_lag = 0

            while time_passed > self.logic_time_elapsed():
                self.state.step(PMOVE)

            self.state.clear_render_flag()
            while not self.state.render_ready:
                self.state.step(PMOVE)

            # print(PMOVE)
            # print(self.state.state, PMOVE)

            self.fill_leds()
            # Flip the display
            pygame.display.flip()
            frames += 1

        # Done! Time to quit.
        pygame.quit()
        end_time = timer()
        duration = end_time - start_time
        fps = frames / duration
        fsm_transitions = self.state.cycles
        logic_fps = fsm_transitions / duration

        print(f'average FPS = {fps}')
        print(f'fsm state transitions = {fsm_transitions}')
        print(f'logical FPS = {logic_fps}')
        print(f'target logical FPS = {self.clocks_per_second}')


if __name__ == '__main__':
    game = Emulator()
    game.run()