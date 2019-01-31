from shared import gui
import socket
import sys
import time
import json
import pdb
import pygame
import collections


# CONSTANTS


CLIENT_FONT = 'Georgia'

SCREEN_SIZE = (600, 500)


# CLASSES


class GameState:
  def __init__(self):
    self.pos = {}
    self.other_players = collections.OrderedDict()
  def get_personal(self):
    return self.pos
  def other_player_pos(self):
    return self.other_players.popitem()[1]
  def register_data(self, server_data):
    self.pos = server_data['game_state']
  def update_other(self, player_positions):
    self.other_players = collections.OrderedDict(player_positions)


class ClientPainter(gui.Painter):
  def update(self, messages):
    if "player" in messages:
      player = self.elements["player"]
      player.update(messages["player"])
      player.draw()

class Player(gui.Entity):
  def __init__(self, visible = True):
    self.pos = (100, 100)
    self.visible = visible
  def update(self, coords):
    self.pos = (coords['x'], coords['y'])
  def draw(self):
    if self.visible:
      self.surf = pygame.Surface((5, 5))
    else:
      self.surf = pygame.Surface((0, 0))
    self.surf.fill((50, 50, 150))



# FUNCTION DEFINITIONS


def send(client_socket, host_address, send_data):
  message_data = json.dumps(send_data)
  client_socket.sendto(message_data.encode(), host_address)

def listen(client_socket):
  try:
    server_message, _server_address = client_socket.recvfrom(1024)
    server_data = json.loads(server_message.decode())
  except socket.error as e:
    server_data = {}
  return server_data

def check_registration(server_data):
  if 'registration' in server_data:
    return server_data['registration']

def extract_player_pos(server_data):
  player_data = json.loads(server_data['game_state'])
  player_id = server_data['player_id']
  player_data.pop(player_id)
  return player_data

def registration_request(client_socket, host_address):
  registration_data = { 'request': 'register' }
  send(client_socket, host_address, registration_data)

def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  client_socket = program_state['client_socket']
  host_address = program_state['host_address']
  gui_messages = {}

  if program_state['registration']:
    server_data = listen(client_socket)
    if server_data:
      gui_messages['player'] = server_data['game_state']
  else:
    server_data = listen(client_socket)
    registration = check_registration(server_data)
    if registration:
      program_state['registration'] = registration
      print("registered!", registration)
    else:
      registration_request(client_socket, host_address)

  return gui_messages

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

def program_state():
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  client_socket.setblocking(0)
  address = '127.0.0.1'
  port = 12345
  return {
    'client_socket': client_socket,
    'host_address': (address, port),
    'game_state': GameState(),
    'registration': None
  }



# STATEMENTS


painter = ClientPainter(SCREEN_SIZE)

client_title = gui.TextField(
  bold=True,
  font=CLIENT_FONT,
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
