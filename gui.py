import pygame
import sys

BACKGROUND_COLOR = (255,255,255)
FONT_NAME = "Georgia"

TEXT_ANTIALIAS = True
TEXT_COLOR = (0,100,0)

HEADER_BOLD = True
HEADER_FONTSIZE = 18


def gui(program_state, business, screen_size):
  pygame.init()
  screen = pygame.display.set_mode(screen_size)

  window = Window(program_state, business, screen)
  window.open()
  main_loop(program_state, business, screen)



class Window:
  def __init__(self, program_state, business, screen):
    self.business = business
    self.header_font = pygame.font.SysFont(FONT_NAME, HEADER_FONTSIZE, HEADER_BOLD)
    self.header_text = self.header_font.render("Hello", TEXT_ANTIALIAS, TEXT_COLOR)
    self.messages = {}
    self.program_state = program_state
    self.screen = screen

  def main_loop(self):
    while True:
      events = pygame.event.get()

      for event in events:
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      self.run_business()
      self.update()

  def open(self):
    self.main_loop()

  def run_business(self):
    self.messages = self.business(program_state=self.program_state)

  def update(self):
    self.screen.fill(BACKGROUND_COLOR)
    self.screen.blit(self.header_text, (200, 200))
    pygame.display.flip()


