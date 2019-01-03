import gui
import socket
import sys
import time
import json
import pdb


def communicate(client_socket, host_address, send_data):
  try:
    server_message, _server_address = client_socket.recvfrom(1024)
    server_data = json.loads(server_message)
  except socket.error as e:
    if e[0] != 35:
      raise e
    server_data = {}
  client_socket.sendto(send_data, host_address)
  return server_data

def extract_player_pos(server_data):
  player_data = json.loads(server_data['game_state'])
  player_id = server_data['player_id']
  player_data.pop(player_id)
  return player_data

def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  client_socket = program_state['client_socket']
  host_address = program_state['host_address']
  game_state = program_state['game_state']
  gui_messages = {}
  client_data = json.dumps({ 'player_pos': game_state.get_personal() })
  server_data = communicate(client_socket, host_address, client_data)
  if server_data:
    game_state.update_other(extract_player_pos(server_data))
  return gui_messages

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

class GameState:
  def __init__(self):
    self.pos = (0,0)
    self.other_players = []
  def update_other(self, player_pos):
    self.other_players = player_pos
  def get_personal(self):
    return self.pos

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
