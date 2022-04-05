import curses

# Import all Data Handlers
import modules.datahandlers

# Import all UI elements
import modules.uielements

client_version = 0.01

requesthandler = modules.datahandlers.requesthandler.RequestHandler()
datahandler = modules.datahandlers.datahandler.DataHandler()
usernamehandler = modules.datahandlers.usernamehandler.UsernameHandler()
inventoryhandler = modules.datahandlers.inventoryhandler.InventoryHandler()

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

    self.requesthandler.username = self.usernamehandler.get_username()
    self.server_name = self.requesthandler.get_server_name()
    self.server_version = self.requesthandler.get_server_version()
    
    encrypted_save = self.requesthandler.cloudsave_get()
    encrypted_save = encrypted_save.encode()

    self.datahandler.save_data = self.datahandler.get_save_file()
    screen.addstr(3, 1, "Loading Property Data")

    self.datahandler.get_property_data()
    screen.addstr(3,1, "Loading Game")

    UserInterface()
  
class UserInterface:
  def __init__(self) -> None:
    self.Dashboard
  
  class Dashboard:
    name, empire_name, money = None, None, None

    def __init__(self) -> None:
      self.init_data()

    def init_data(self):
      self.name = datahandler.get_name()
      self.empire_name = datahandler.get_empirename()
      self.money = datahandler.get_money()
    
    # Remember the coords are y, x

    def render(self):
      screen.clear()
      screen.addstr(0, 0, f"{self.empire_name} Dashboard")
      screen.addstr(1, 0, f"Welcome back {self.name}")
      screen.addstr(4, 0, "Business Statistics")

      # Renders the business statistics

      screen.addstr(5, 2, f"Capital: {self.money}")

      # Renders property options

      screen.addstr(4, 6, "Property Portfolio Management")
      screen.addstr(5, 6, "View [p]roperty Portfolio")
      screen.addstr(6, 6, "Visit the property [m]arket")

      # Renders other options

      screen.addstr(9, 0, "[H]elp")
      screen.addstr(9, 8, "[E]dit Business Documents")

      screen.refresh()
    
    def handle_keypress(self):
      key_press = self.screen.get_wch()

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
    pass

  class GameHelp:
    pass

  class BusinessIdentityManagement:
    pass