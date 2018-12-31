import gui
import socket

def business_procedure(events, program_state):
  socket_object = program_state['socket']
  c, addr = socket_object.accept()
  print 'Got connection from', addr
  c.send('Thank you for connecting')
  c.close()

def business_function():
  return lambda events, program_state: business_procedure(events, program_state)

def program_state():
  socket_object = socket.socket()
  host = 'localhost'
  port = 12345
  print 'hostname: ', host
  print 'port: ', port
  socket_object.bind((host, port))
  socket_object.listen(5)
  return {
    'socket': socket_object
  }

screen_size = (500, 600)
initial_state = program_state()
gui.main(initial_state, business_function(), screen_size)
