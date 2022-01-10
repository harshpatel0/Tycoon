from cryptography.fernet import Fernet
import os
import curses
from time import sleep

def check_key(self):
  if os.path.exists('key.dat'):
    return True
  else:
    return False

class Keys():

  key = b""

  def check_key(self):
    if os.path.exists(f'{os.getcwd()}\\key.dat'):
      return True
    else:
      return False

  def generate_key(self):
    self.key = Fernet.generate_key()
    self.save_key()
    return self.key
    
  def load_key(self):
    with open(f"{os.getcwd()}\\key.dat",'r') as keyfile:
      self.key = keyfile.read().encode()
      return self.key
  
  def save_key(self):
    with open(f"{os.getcwd()}\\key.dat",'w') as keyfile:
      keyfile.write(self.key.decode())
    
    return None
    
class KeyDashboard(Keys):
  def __init__(self) -> None:
    super().__init__()
    self.dashboard()
  
  def render_dashboard(self,screen):

    # y, x

    screen.clear()
    screen.addstr(1,1, f"Server Key Dashboard")
    screen.addstr(3, 6, f"Key: {self.load_key()}")
    screen.addstr(5, 6, f"Key Options")
    screen.addstr(6, 6, f"[R]eset Key")
    screen.addstr(7, 6, f"E[x]it")
  
  def render_reset_warning(self, screen):
    screen.clear()
    screen.addstr(1,1, f"Server Key Dashboard > Reset Key")
    screen.addstr(3, 6, f"WARNING")
    screen.addstr(4, 6, "*" * len('warning'))
    screen.addstr(6, 6, f"Reseting your key will cause save files to not be able to be decrypted therefore")
    screen.addstr(7, 6, f"they will be unusable and will cause issues to the client")

    screen.addstr(9,6, "Press [y] to continue and renew keys")
    screen.addstr(10,6, "Press [n] to deny and go back")

  def render_reset_final_screen(self, screen):
    screen.clear()
    screen.addstr(1,1, f"Server Key Dashboard > Reset Key")
    screen.addstr(3, 6, f"Success")
    screen.addstr(4, 6, "*" * len('success'))
    screen.addstr(6, 6, f"Your new key is {self.key}")
    screen.addstr(7, 6, f"This key is saved in 'key.dat' in the server folder")

    screen.addstr(9,12, "This message will autoclose in 3 seconds")

  
  def reset_key_screen(self, screen):
    while True:
      self.render_reset_warning(screen)
      screen.refresh()

      event = screen.getch()
      key_pressed = chr(event)

      if key_pressed == 'y':
        self.generate_key()
        while True:
          self.render_reset_final_screen(screen)
          screen.refresh()

          sleep(3)
          break
      
      if key_pressed == 'n':
        pass

      return None
    
  
  def dashboard(self):
    screen = curses.initscr()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.curs_set(0)

    if self.check_key() == False:
      self.generate_key()
    else:
      self.load_key()

    while True:
      self.render_dashboard(screen)
      screen.refresh()

      event = screen.getch()
      key_pressed = chr(event)

      if key_pressed == 'x':
        break
      if key_pressed == 'r':
        self.reset_key_screen(screen)
    
    quit()
if __name__ == "__main__":
  KeyDashboard()