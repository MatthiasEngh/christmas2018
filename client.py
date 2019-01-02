import gui
import socket
import sys
import time


def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  client_socket = program_state['client_socket']
  host_address = program_state['host_address']
  client_socket.sendto("asdf", host_address)

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

def program_state():
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  address = '127.0.0.1'
  port = 12345
  return {
    'client_socket': client_socket,
    'host_address': (address, port)
  }


screen_size = (600, 500)

class ClientPainter(gui.Painter):
  def update(self, messages):
    pass

painter = ClientPainter(screen_size)

client_font = 'Georgia'
client_title = gui.TextField(
  bold=True,
  font=client_font,
  pos=(10,10),
  font_size=20,
  text="Client"
)
painter.add_element("title", client_title)

gui.gui(program_state(), business_function(), painter)
