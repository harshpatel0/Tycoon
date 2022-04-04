import curses

# Import all Data Handlers
import modules.datahandlers as datahandlers

# Import all UI elements
import modules.uielements as uielements

client_version = 0.01

requesthandler = datahandlers.requesthandler.RequestHandler()
datahandler = datahandlers.datahandler.DataHandler()
usernamehandler = datahandlers.usernamehandler.UsernameHandler()
inventoryhandler = datahandlers.inventoryhandler.InventoryHandler()

screen = curses.initscr()

# State Variables
connected = False

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
    ipaddress_textbox = uielements.textboxes.AddressTextBox()

    ipaddress = ipaddress_textbox.create_textbox("Server Address", (1,1), 19)
    screen.clear()    
    screen.addstr(1,2, f"Connecting to {ipaddress}")
    screen.refresh()

    self.requesthandler.server_url = ipaddress
    status = self.requesthandler.ping()

    if status != "NO_CONNECTION":
      screen.clear()
      connected = True

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
    self.render_ui()
  
  def render_ui(self):
    pass