import gui
import socket
import sys
import time
import json

def communicate(client_socket, host_address, send_data):
  try:
    server_message, _server_address = client_socket.recvfrom(1024)
    server_data = json.loads(server_message)
  except socket.error:
    server_data = {}
  client_socket.sendto(send_data, host_address)
  return server_data

def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  client_socket = program_state['client_socket']
  host_address = program_state['host_address']
  game_state = program_state['game_state']
  server_data = communicate(client_socket, host_address, json.dumps(game_state.get_personal()))
  if 'game_state' in server_data:
    game_state.accept(server_data['game_state'])


def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

class GameState:
  def __init__(self):
    pass
  def accept(self, server_state):
    pass
  def get_personal(self):
    return {}

def program_state():
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  client_socket.setblocking(0)
  address = '127.0.0.1'
  port = 12345
  return {
    'client_socket': client_socket,
    'host_address': (address, port),
    'game_state': GameState()
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
