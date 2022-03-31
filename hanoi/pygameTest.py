# Simple pygame program

# Import and initialize the pygame library
import pygame

from pygame.locals import *
from GameMachine import GameMachine

state_machine = GameMachine()
pygame.init()

# Set up the drawing window

X_LEDS, Y_LEDS = 32, 8
X_BUFFER, Y_BUFFER = 128, 128
LED_SIZE = 32

screen = pygame.display.set_mode([
    2 * X_BUFFER + X_LEDS * LED_SIZE,
    2 * Y_BUFFER + Y_LEDS * LED_SIZE
])

BLACK = (0, 0, 0)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with gray
    screen.fill((100, 100, 100))

    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    num_pixels = X_LEDS * Y_LEDS

    for k in range(num_pixels):
        x, y, = k % X_LEDS, k // X_LEDS
        pygame.draw.rect(screen, BLACK, rect=(
            X_BUFFER + x * LED_SIZE, Y_BUFFER + y * LED_SIZE,
            LED_SIZE - 1, LED_SIZE - 1
        ))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()