import gui
import select
import socket
import time

import pdb


CONNECTION_MESSAGE = '%s: Got connection from %s'
CLIENT_MESSAGE = 'Thank you for connecting'
SOCKET_TIMEOUT = 0.2
TERMINAL_PRINT = True


def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  gui_messages = {
    'log': []
  }
  readable_sockets, _, _ = select.select(program_state['sockets'], [], [], SOCKET_TIMEOUT)
  for readable_socket in readable_sockets:
    if readable_socket is program_state['server_socket']:
      c, addr = readable_socket.accept()
      log_message = CONNECTION_MESSAGE % (time.ctime(), str(addr))
      gui_messages['log'].append(log_message)
      print log_message
      c.send(CLIENT_MESSAGE)
      c.close()
    else:
      pass
  return gui_messages

def business_function():
  return lambda **kwargs: business_procedure(**kwargs)

def program_state():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  host = socket.gethostname()
  port = 12345
  print 'hostname: ', host
  print 'port: ', port
  server_socket.bind((host, port))
  server_socket.listen(5)
  return {
    'sockets': [server_socket],
    'server_socket': server_socket
  }


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

message_element = gui.TextField(
  bold=False,
  font=log_font,
  pos=(10,50),
  font_size=14,
  text=""
)
painter.add_element("message", message_element)

gui.gui(initial_state, business_function(), painter)
