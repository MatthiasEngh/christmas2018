import gui
import select
import socket
import time



RECEIVE_MESSAGE = '%s: Got "%s" from %s'
CLIENT_MESSAGE = 'Thank you for connecting'
SOCKET_TIMEOUT = 0.2
TERMINAL_PRINT = True


def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  shared_state = program_state['shared_state']
  server_socket = program_state['server_socket']
  gui_messages = {
  }
  received_data = receive_data(server_socket)
  if 'message' in received_data:
    message = RECEIVE_MESSAGE % (received_data['time'], received_data['message'], received_data['from'])
    shared_state.add(message)
    print shared_state.messages
  return gui_messages

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

MESSAGES_LENGTH = 10
class ServerSharedState:
  def __init__(self):
    self.messages = []
  def add(self, message):
    if len(self.messages) >= MESSAGES_LENGTH:
      del(self.messages[0])
    self.messages.append(message)

def program_state():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  server_socket.setblocking(0)
  host = socket.gethostname()
  port = 12345
  print 'hostname: ', host
  print 'port: ', port
  server_socket.bind((host, port))
  return {
    'sockets': [server_socket],
    'server_socket': server_socket,
    'shared_state': ServerSharedState()
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
