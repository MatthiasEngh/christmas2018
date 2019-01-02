import gui
import socket
import sys
import time


def business_procedure(**kwargs):
  program_state = kwargs['program_state']
  client_socket = program_state['client_socket']
  client_socket.connect(program_state['connection_details'])
  print client_socket.recv(1024)
  client_socket.close()
  for i in range(3):
    print "shutting down in ", 3 - i, "seconds.."
    time.sleep(1)
  sys.exit()

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
painter = gui.Painter(screen_size)
gui.gui(program_state(), business_function(), painter)
