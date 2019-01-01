import gui
import select
import socket


CONNECTION_MESSAGE = 'Got connection from %s'
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
      gui_messages['log'].append(CONNECTION_MESSAGE % str(addr))
      if TERMINAL_PRINT:
        print CONNECTION_MESSAGE % str(addr)
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
gui.gui(initial_state, business_function(), screen_size)
