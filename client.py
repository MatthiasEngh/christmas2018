import gui

def business_procedure(program_state):
  pass

def business_function():
  return lambda: business_procedure()

def program_state():
  return None

screen_size = (600, 500)
gui.main(program_state(), business_function(), screen_size)
