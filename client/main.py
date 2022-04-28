import curses
from time import sleep
from sys import exit
# # Import all Data Handlers
# import modules.datahandlers

import modules.datahandlers.backendhandler
import modules.datahandlers.datahandler
import modules.datahandlers.requesthandler
import modules.datahandlers.usernamehandler

import modules.uielements.textboxes
# # Import all UI elements
# import modules.uielements

client_version = 0.01

# requesthandler = modules.datahandlers.requesthandler.RequestHandler()
# usernamehandler = modules.datahandlers.usernamehandler.UsernameHandler()
# datahandler = modules.datahandlers.datahandler.DataHandler()

requesthandler = modules.datahandlers.requesthandler.RequestHandler()
datahandler = modules.datahandlers.datahandler.DataHandler()
usernamehandler = modules.datahandlers.usernamehandler.UsernameHandler()

global screen
screen = curses.initscr()

# Server Data 
server_version = None
server_name = None

class Main():
  def __init__(self) -> None:
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0) 
    screen.keypad(True)
  
  def connect_to_server(self):
    ipaddress_textbox = modules.uielements.textboxes.AddressTextBox(screen=screen)

    ipaddress = ipaddress_textbox.create_textbox("Server Address", (1,1), 19)
    screen.clear()    
    screen.addstr(1,2, f"Connecting to {ipaddress}")
    screen.refresh()

    self.requesthandler.server_url = ipaddress
    status = self.requesthandler.ping()

    if status != "NO_CONNECTION":
      screen.clear()

    else:
      screen.clear()

      screen.addstr(1, 2, f"Couldn't connect to {ipaddress}")
      screen.addstr(2, 4, "A connection to a server is needed to play")
      screen.addstr(3, 4, "[R]etry, Any other key to exit")

      screen.refresh()

      keypress = screen.get_wch()

      if keypress == "r":
        self.requesthandler.server_url = None
        self.connect_to_server()
      else:
        curses.endwin()
        quit()
    
  def retrieve_server_data(self):
    screen.clear()

    screen.addstr(0,0, "Loading")
    screen.addstr(1,0, "-------")
    screen.addstr(3,1, "Loading Save file")
    screen.refresh()

    self.requesthandler.username = self.usernamehandler.get_username()
    self.server_name = self.requesthandler.get_server_name()
    self.server_version = self.requesthandler.get_server_version()
    
    # encrypted_save = self.requesthandler.cloudsave_get()
    # encrypted_save = encrypted_save.encode()

    # Handled by datahandler.get_save_file() function

    if self.datahandler.get_save_file() != "INCORRECT KEY":
      screen.addstr(3, 1, "Loading Property Data")
      screen.refresh()

      self.datahandler.get_property_data()
      screen.addstr(3,1, "Loading Game")
      screen.refresh()

      UserInterface()
    
    screen.addstr(0, 0, "Loading Failed")
    screen.addstr(1, 0, "--------------")
    screen.addstr(3, 1, "The save file couldn't be decrypted by the key from the")
    screen.addstr(4, 1, "server, the key might have changed, unfortunately there")
    screen.addstr(5, 1, "is no way to get your previous save file back unless the")
    screen.addstr(6, 1, "old key is backed up, contact the server host for help.")
    screen.addstr(8, 1, "The game can not be launched, quit the game by pressing q")

    screen.refresh()

    while screen.get_wch() != "q":
      pass
    exit()

      
  
class UserInterface:
  def __init__(self) -> None:
    self.Dashboard
  
  class Dashboard:
    name, empire_name, money, property_count = None, None, None, None

    def __init__(self) -> None:
      screen.clear()
      self.init_data()
      self.render()
      self.handle_keypress()

    def init_data(self):
      self.name = datahandler.name
      self.empire_name = datahandler.empire_name
      self.money = datahandler.money
      self.property_count = datahandler.property_count

    # Remember the coords are y, x

    def render(self):
      screen.clear()
      screen.addstr(0, 0, f"{self.empire_name} Dashboard")
      screen.addstr(1, 0, f"Welcome back {self.name}")
      screen.addstr(4, 0, "Business Statistics")

      # Renders the business statistics

      # y, x
      screen.addstr(5, 2, f"Capital: {self.money}")
      screen.addstr(6, 2, f"Properties: {self.property_count}")


      # Renders property options

      screen.addstr(4, 6, "Property Portfolio Management")
      screen.addstr(5, 6, "View [p]roperty Portfolio")
      screen.addstr(6, 6, "Visit the property [m]arket")

      # Renders other options

      screen.addstr(9, 0, "[H]elp")
      screen.addstr(9, 8, "[E]dit Business Documents")

      screen.refresh()
    
    def handle_keypress(self):
      key_press = screen.get_wch()

      if key_press == 'p':
        UserInterface.PropertyPortfolio
      if key_press == 'm':
        UserInterface.PropertyMarket
      if key_press == 'h':
        UserInterface.GameHelp
      if key_press == 'e':
        UserInterface.BusinessIdentityManagement
  
  class PropertyPortfolio:
    pass

  class PropertyMarket:
    money, property_count = None, None
    
    # This will be used to see which property to load and what property the user has chosen to bought
    page = 0
  
    # Property Data
    properties = datahandler.property_data

    def __init__(self) -> None:
      screen.clear()
      self.init_data()
      # self.render() # Special case
      self.data_gatherer()
      # self.handle_keypress() # Handled in render funcyion

    def init_data(self):
      self.money = datahandler.money
      self.property_count = datahandler.property_count
    
    def data_gatherer(self):
      # First get the keys
      key_list = tuple(self.properties.keys())
      # Then get the one we want to get
      try:
        data = self.properties[key_list[self.page]]
      except IndexError:
        # Here the page variable has passed higher than what the list actually has
        self.page = len(key_list) - 1
        data = self.properties[key_list[self.page]]

      # Data is assembled here before sending
      page = self.page
      name = data['name']
      cost = data['cost']
      location = data['location']
      set = data['set']
      max_page = len(key_list)

      self.render(page, name, cost, location, set, max_page)
    
    def render(self, page: int, name: str, cost: int, location: str, set: str, max_page: str):
      screen.clear()
                  # y,x 
      screen.addstr(0,0, "[B]ack\t\tProperty Market")        
      screen.addstr(1,0, "---------------------------------")
      screen.addstr(2,0, f"Page: {page}")
      screen.addstr(4,0, f"{name}")
      screen.addstr(5,0, f'TY${cost}')
      screen.addstr(6,0, f'Located in: {location}\tPart of {set} set')

      # Key help

      def determine_nav_key():
        if page == 0:
          return "[->]Next Page"
        if page == max_page:
          return "[<-]Previous Page"
        if page != 0 and page != max_page:
          return "[<-]Previous Page\t[->]Next Page"

      screen.addstr(7,0, len(f'Located in: {location}\tPart of {set} set') * '-')
      screen.addstr(8,0, f"[b]uy\t{determine_nav_key()}")

      self.handle_keypress()

    def handle_keypress(self):
      # Keys
      next_key = 454
      previous_key = 452
      buy_key = 'b'
      quit_key = '.'

      key_press = screen.get_wch()

      if key_press == next_key:
        self.page = self.page + 1
        self.data_gatherer()
      
      if key_press == previous_key:
        if self.page != 0:
          self.page = self.page - 1
          self.data_gatherer()
        else:
          self.handle_keypress()
      
      if key_press == quit_key:
        UserInterface.Dashboard()
      
      if key_press == buy_key:
        pass


  class GameHelp:
    pass

  class BusinessIdentityManagement:
    pass


def main():
  main = Main()
  main.connect_to_server()

if __name__ == '__main__':
  main()