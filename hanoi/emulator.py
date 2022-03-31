# Import and initialize the pygame library
import pygame

from enum import Enum
from pygame.locals import *
from GameMachine import GameMachine
from BitNumber import *

X_LEDS, Y_LEDS = 32, 8
X_BUFFER, Y_BUFFER = 128, 128
LED_SIZE = 32

class Colors(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    PLAYER = (255, 0, 0)


class Emulator(object):
    def __init__(self):
        self.state_machine = GameMachine()
        self.screen = None

    def init_screen(self):
        self.screen = pygame.display.set_mode([
            2 * X_BUFFER + X_LEDS * LED_SIZE,
            2 * Y_BUFFER + Y_LEDS * LED_SIZE
        ])

        return self.screen

    def fill_leds(self):
        num_pixels = X_LEDS * Y_LEDS

        for k in range(num_pixels):
            x, y, = k % X_LEDS, k // X_LEDS

            led_color = Colors.BLACK
            player_pos: UBitNumber = self.state_machine.player_pos
            player_x, player_y = self.extract_position(player_pos)
            # print(f'{player_x, player_y}')

            if (player_x == x) and (player_y == y):
                led_color = Colors.PLAYER

            led_color = led_color.value
            pygame.draw.rect(self.screen, led_color, rect=(
                X_BUFFER + x * LED_SIZE, Y_BUFFER + y * LED_SIZE,
                LED_SIZE - 1, LED_SIZE - 1
            ))

    @staticmethod
    def extract_position(bit_position: UBitNumber):
        # decode the 8 bit position register into x and y
        # integer coordinates respectively
        x, y = int(bit_position[4:0]), int(bit_position[7:5])
        return x, y

    def run(self):
        pygame.init()
        self.init_screen()
        running = True

        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Fill the background with gray
            self.screen.fill((100, 100, 100))
            self.fill_leds()

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()


if __name__ == '__main__':
    game = Emulator()
    game.run()