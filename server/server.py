import json
from shared import gui
import re
import select
import socket
import time
import uuid



# CONSTANTS


CLIENT_MESSAGE = 'Thank you for connecting'
MESSAGES_LENGTH = 10
RECEIVE_MESSAGE = '%s: Got "%s" from %s'
SOCKET_TIMEOUT = 0.2
TERMINAL_PRINT = True



# CLASSES


class Game:
  def __init__(self):
    self.players = {}
  def generate_uuid(self):
    return str(uuid.uuid4())
  def interpret(self, network_data):
    data = self.parse_message(network_data['message'])
  def parse_message(self, message):
    return json.loads(message)
  def register_player(self, address):
    player_uuid = self.generate_uuid()
    self.players[player_uuid] = { 'address': address }
    print("registered player", player_uuid)
    return player_uuid

class ServerPainter(gui.Painter):
  def update(self, messages):
    pass



# FUNCTION DEFINITIONS

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  server_socket = program_state['server_socket']
  game = program_state['game']
  gui_messages = {}

  message, address, timestamp = receive_data(server_socket)

  if not message:
    return gui_messages

  data = json.loads(message)
  
  if not 'request' in data:
    return gui_messages

  if data['request'] == 'register':
    registration_id = game.register_player(address)
    message = json.dumps({ 'registration': registration_id })
    server_socket.sendto(message.encode(), address)

  if data['request'] == 'message':
    pass

  return gui_messages

def program_state():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server_socket.setblocking(0)
  host = socket.gethostname()
  port = 12345
  print('hostname: ', host)
  print('port: ', port)
  server_socket.bind((host, port))
  return {
    'game': Game(),
    'server_socket': server_socket,
  }

def receive_data(server_socket):
  try:
    message, address = server_socket.recvfrom(1024)
    timestamp = time.ctime()
    network_data = (message, address, timestamp)
  except socket.error:
    network_data = (None, None, None)
  return network_data



# STATEMENTS


screen_size = (500, 600)
initial_state = program_state()

painter = ServerPainter(screen_size)
log_font = "Geogia"

header_element = gui.TextField(
  bold=True,
  font=log_font,
  pos=(10,10),
  font_size=18,
  text="Server"
)
painter.add_element("header", header_element)

fields = {}
for i in range(MESSAGES_LENGTH):
  fields["f%s" % i] = gui.TextField(
    bold = False,
    font=log_font,
    font_size=14,
    pos=(10, 50),
    text="elem%s" % i
  )
connection_list = gui.ListField(
  bold=False,
  fields=fields,
  font=log_font,
  font_size=14,
  pos=(10, 200)
)

painter.add_element("log", connection_list)

gui.gui(initial_state, business_function(), painter)
