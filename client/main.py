import curses
from time import sleep
from sys import exit
# Import all Data Handlers
import modules.datahandlers

# Import all UI elements
import modules.uielements

client_version = 0.01

requesthandler = modules.datahandlers.requesthandler.RequestHandler()
usernamehandler = modules.datahandlers.usernamehandler.UsernameHandler()
datahandler = modules.datahandlers.datahandler.DataHandler()

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
    ipaddress_textbox = modules.uielements.textboxes.AddressTextBox()

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

    def __init__(self) -> None:
      screen.clear()
      self.init_data()
      self.render()
      # self.handle_keypress()

    def init_data(self):
      self.money = datahandler.money
      self.property_count = datahandler.property_count
    
    def render(self):
      # y,x 
      screen.addstr(0,0, "[B]ack\t\tProperty Market")        
      screen.addstr(1,0, "---------------------------------")
      # Deal with this later

  class GameHelp:
    pass

  class BusinessIdentityManagement:
    pass