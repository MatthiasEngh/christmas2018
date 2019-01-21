import json
import gui
import select
import socket
import time



RECEIVE_MESSAGE = '%s: Got "%s" from %s'
CLIENT_MESSAGE = 'Thank you for connecting'
SOCKET_TIMEOUT = 0.2
TERMINAL_PRINT = True


def extract_player_pos(message):
  player_pos = json.loads(message)['player_pos']
  return player_pos

def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  game_state = program_state['game_state']
  server_socket = program_state['server_socket']
  client_pool = program_state['client_pool']
  gui_messages = {
  }
  received_data = receive_data(server_socket)
  if 'message' in received_data:
    client_address = received_data['from']
    if client_pool.is_new(client_address):
      client_id = client_pool.add(client_address)
      game_state.add_player(client_id, extract_player_pos(received_data['message']))
  client_pool.send(game_state.client_data())
  return gui_messages

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

class Client:
  def __init__(self, address):
    self.address = address
  def id(self):
    return str(self.address)

class ClientPool:
  def __init__(self, socket):
    self.clients = {}
    self.socket = socket
  def add(self, client_address):
    print("adding client with", client_address)
    new_client = Client(client_address)
    self.clients[client_address] = new_client
    return new_client.id()
  def is_new(self, client_address):
    return client_address not in self.clients
  def send(self, client_data):
    game_state = json.dumps(client_data)
    for client_address, client in self.clients.items():
      message_data = {
        'game_state': game_state,
        'player_id': client.id()
      }
      message = json.dumps(message_data)
      self.socket.sendto(message.encode(), client_address)

MESSAGES_LENGTH = 10
class GameState:
  def __init__(self):
    self.players = {}
  def add_player(self, player_id, player_pos):
    self.players[player_id] = player_pos
  def client_data(self):
    return self.players

def program_state():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server_socket.setblocking(0)
  host = socket.gethostname()
  port = 12345
  print('hostname: ', host)
  print('port: ', port)
  server_socket.bind((host, port))
  return {
    'client_pool': ClientPool(server_socket),
    'server_socket': server_socket,
    'game_state': GameState(),
    'sockets': [server_socket],
  }

def receive_data(server_socket):
  try:
    message, address = server_socket.recvfrom(1024)
    timestamp = time.ctime()
    network_data = {
      'from': address,
      'message': message,
      'time': timestamp
    }
  except socket.error:
    network_data = {}
  return network_data


screen_size = (500, 600)
initial_state = program_state()

class ServerPainter(gui.Painter):
  def update(self, messages):
    pass

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
