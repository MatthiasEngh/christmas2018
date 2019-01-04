import gui
import socket
import sys
import time
import json
import pdb
import pygame
import collections


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
  if any(game_state.other_players):
    gui_messages["other_player"] = {
      "pos": game_state.other_player_pos(),
      "visible": True
    }
  return gui_messages

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

class GameState:
  def __init__(self):
    self.pos = (150,150)
    self.other_players = collections.OrderedDict()
  def update_other(self, player_positions):
    self.other_players = collections.OrderedDict(player_positions)
  def get_personal(self):
    return self.pos
  def other_player_pos(self):
    return self.other_players.popitem()[1]

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
    if "other_player" in messages:
      other_player = self.elements["other_player"]
      other_player.pos = messages["other_player"]["pos"]
      other_player.visible = messages["other_player"]["visible"]
      other_player.draw()

class Player(gui.Entity):
  def __init__(self, visible = True):
    self.pos = (100, 100)
    self.visible = visible
  def update(self, **kwargs):
    pass
  def draw(self):
    if self.visible:
      self.surf = pygame.Surface((5, 5))
    else:
      self.surf = pygame.Surface((0, 0))
    self.surf.fill((50, 50, 150))

painter = ClientPainter(screen_size)

client_font = 'Georgia'
client_title = gui.TextField(
  bold=True,
  font=client_font,
  pos=(10, 10),
  font_size=20,
  text="Client"
)
player = Player()
other_player = Player(False)
painter.add_element("title", client_title)
painter.add_element("player", player)
painter.add_element("other_player", other_player)

gui.gui(program_state(), business_function(), painter)
