import gui
import socket
import sys
import time


def connect(client_socket, connection_details):
  client_socket.connect(connection_details)
  print client_socket.recv(1024)
  client_socket.close()
  for i in range(3):
    print "shutting down in ", 3 - i, "seconds.."
    time.sleep(1)
  sys.exit()


def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  if False:
    connect(program_state['client_socket'], program_state['connection_details'])

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

def program_state():
  client_socket = socket.socket()
  host = socket.gethostname()
  port = 12345
  return {
    'client_socket': client_socket,
    'connection_details': (host, port)
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
