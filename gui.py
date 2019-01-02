import pygame
import sys

BACKGROUND_COLOR = (255,255,255)
FONT_NAME = "Georgia"

TEXT_ANTIALIAS = True
TEXT_COLOR = (0,100,0)

HEADER_BOLD = True
HEADER_FONTSIZE = 18


def gui(program_state, business, painter):
  pygame.init()
  painter.configure()

  window = Window(program_state, business, painter)
  window.open()

class TextField:
  def __init__(self, **kwargs):
    self.bold = kwargs['bold']
    self.font = kwargs['font']
    self.font_size = kwargs['font_size']
    self.pos = kwargs['pos']
    self.text = kwargs['text']

  def configure(self):
    self.font = pygame.font.SysFont(self.font, self.font_size, self.bold)
    self.surf = self.font.render(self.text, TEXT_ANTIALIAS, TEXT_COLOR)


class Painter:
  def __init__(self, screen_size):
    self.elements = []
    self.fonts = {}
    self.font_details = {}
    self.screen_size = screen_size

  def add_element(self, element):
    self.elements.append(element)

  def configure(self):
    self.screen = pygame.display.set_mode(self.screen_size)
    for element in self.elements:
      element.configure()

  def paint(self):
    self.screen.fill(BACKGROUND_COLOR)
    for element in self.elements:
      self.screen.blit(element.surf, element.pos)


class Window:
  def __init__(self, program_state, business, painter):
    self.business = business
    self.messages = {}
    self.program_state = program_state
    self.painter = painter

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
    self.painter.paint()
    pygame.display.flip()


