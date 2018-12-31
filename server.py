import gui
import select
import socket

def business_procedure(events, program_state):
  readable_sockets, _, _ = select.select(program_state['sockets'], [], [], 0.5)
  for readable_socket in readable_sockets:
    if readable_socket is program_state['server_socket']:
      c, addr = readable_socket.accept()
      print 'Got connection from', addr
      c.send('Thank you for connecting')
      c.close()
    else:
      pass

def business_function():
  return lambda events, program_state: business_procedure(events, program_state)

def program_state():
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  host = 'localhost'
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
gui.main(initial_state, business_function(), screen_size)
