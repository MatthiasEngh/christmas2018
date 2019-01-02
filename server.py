import gui
import select
import socket
import time

import pdb


RECEIVE_MESSAGE = '%s: Got "%s" from %s'
CLIENT_MESSAGE = 'Thank you for connecting'
SOCKET_TIMEOUT = 0.2
TERMINAL_PRINT = True


def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  gui_messages = {
    'log': []
  }
  received_data = receive_data(program_state)
  if 'message' in received_data:
    message = RECEIVE_MESSAGE % (received_data['time'], received_data['message'], received_data['from'])
    gui_messages['log'].append(message)
  return gui_messages

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

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
    'server_socket': server_socket
  }

def receive_data(program_state):
  try:
    message, address = program_state['server_socket'].recvfrom(1024)
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
    if "log" in messages and len(messages["log"]) > 0:
      message_text = messages["log"][-1]
      self.elements["message"].update(text = message_text)

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

element1 = gui.TextField(
  bold = False,
  font=log_font,
  font_size=14,
  pos=(10, 50),
  text="elem1"
)
element2 = gui.TextField(
  bold = False,
  font=log_font,
  font_size=14,
  pos=(10, 50),
  text="elem2"
)
connection_list = gui.ListField(
  bold=False,
  fields=[
    element1,
    element2
  ],
  font=log_font,
  font_size=14,
  pos=(10, 200)
)

message_element = gui.TextField(
  bold=False,
  font=log_font,
  pos=(10,50),
  font_size=14,
  text=""
)
painter.add_element("message", message_element)
painter.add_element("log", connection_list)

gui.gui(initial_state, business_function(), painter)
