import pygame
import sys

BACKGROUND_COLOR = (255,255,255)
FONT_NAME = "Georgia"

TEXT_ANTIALIAS = True
TEXT_COLOR = (0,0,0)

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
    self.draw()

  def draw(self):
    self.surf = self.font.render(self.text, TEXT_ANTIALIAS, TEXT_COLOR)

  def update(self, **kwargs):
    self.text = kwargs['text']
    self.draw()

class ListField:
  def __init__(self, **kwargs):
    self.bold = kwargs['bold']
    if 'list' in kwargs:
      self.list = kwargs['list']
    else:
      self.list = []
    self.font = kwargs['font']
    self.font_size = kwargs['font_size']
    self.pos = kwargs['pos']
    if 'fields' in kwargs:
      self.text_fields = kwargs['fields']
    else:
      self.text_fields = []

  def configure(self):
    self.font = pygame.font.SysFont(self.font, self.font_size, self.bold)
    for text_field in self.text_fields:
      text_field.configure()
    self.draw()

  def element_count(self):
    return len(self.text_fields)

  def getheight(self):
    return 500

  def getsize(self):
    return (self.getwidth(), self.getheight())

  def getwidth(self):
    return 100

  def draw(self):
    self.surf = pygame.Surface(self.getsize())
    self.surf.fill((255,255,255))
    for i in range(self.element_count()):
      self.surf.blit(self.text_fields[i].surf, self.element_pos(i))

  def element_pos(self, num):
    return (20, num * 50)

  def update(self, **kwargs):
    pass

class Painter:
  def __init__(self, screen_size):
    self.elements = {}
    self.fonts = {}
    self.font_details = {}
    self.screen_size = screen_size

  def add_element(self, element_name, element):
    self.elements[element_name] = element

  def configure(self):
    self.screen = pygame.display.set_mode(self.screen_size)
    for element_name, element in self.elements.iteritems():
      element.configure()

  def paint(self):
    self.screen.fill(BACKGROUND_COLOR)
    for element_name, element in self.elements.iteritems():
      self.screen.blit(element.surf, element.pos)

  def update(self, messages):
    pass


class Window:
  def __init__(self, program_state, business, painter):
    self.business = business
    self.program_state = program_state
    self.painter = painter

  def main_loop(self):
    while True:
      events = pygame.event.get()

      for event in events:
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      messages = self.run_business()
      self.update(messages)

  def open(self):
    self.main_loop()

  def run_business(self):
    return self.business(program_state=self.program_state)

  def update(self, messages):
    self.painter.update(messages)
    self.painter.paint()
    pygame.display.flip()


