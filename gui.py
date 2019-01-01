import pygame
import sys

def main_loop(program_state, business):
  while True:
    events = pygame.event.get()

    for event in events:
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    business(events, program_state)


def gui(program_state, business, screen_size):
  pygame.init()
  screen = pygame.display.set_mode(screen_size)
  main_loop(program_state, business)

