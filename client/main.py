import curses

# Custom Handlers
import requesthandler
import datahandler
import usernamehandler
import inventoryhandler

# UI Elements
import uielements.textboxes

client_version = 0.01

class Main():
  
  screen = curses.initscr()

  # Handler Modules

  requesthandler = requesthandler.RequestHandler()
  datahandler = datahandler.DataHandler()
  usernamehandler = usernamehandler.UsernameHandler()
  inventoryhandler = inventoryhandler.InventoryHandler()

  # State Variables

  connected = False

  # Server Data 

  server_version = None
  server_name = None

  def __init__(self) -> None:
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0) 
    self.screen.keypad(True)
  
  def connect_to_server(self):
    ipaddress_textbox = uielements.textboxes.AddressTextBox()

    ipaddress = ipaddress_textbox.create_textbox("Server Address", (1,1), 19)
    self.screen.clear()    
    self.screen.addstr(1,2, f"Connecting to {ipaddress}")
    self.screen.refresh()

    self.requesthandler.server_url = ipaddress
    status = self.requesthandler.ping()

    if status == "NO_CONNECTION":
      self.screen.clear()

      self.screen.addstr(1, 2, f"Couldn't connect to {ipaddress}")
      self.screen.addstr(2, 4, "A connection to a server is needed to play")
      self.screen.addstr(3, 4, "[R]etry, Any other key to exit")

      self.screen.refresh()

      keypress = self.screen.get_wch()

      if keypress == "r":
        self.requesthandler.server_url = None
        self.connect_to_server()
      else:
        curses.endwin()
        quit()

    else:
      self.screen.clear()
      return "CONNECTED"
    
  def retrieve_server_data(self):
    self.screen.clear()

    self.screen.addstr(0,0, "Loading")
    self.screen.addstr(1,0, "-------")
    self.screen.addstr(3,1, "Loading Save file")

    self.requesthandler.username = self.usernamehandler.get_username()
    self.server_name = self.requesthandler.get_server_name()
    self.server_version = self.requesthandler.get_server_version()
    
    encrypted_save = self.requesthandler.cloudsave_get()
    encrypted_save = encrypted_save.encode()

    self.datahandler.save_data = self.datahandler.get_save_file()

    self.screen.addstr(3, 1, "Loading Property Data")

    self.datahandler.get_property_data()
    
    self.screen.addstr(3,1, "Loading Game         ")


    # TODO: Finish shit here