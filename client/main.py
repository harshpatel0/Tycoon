print("Loading Files")
import curses
from time import sleep
from sys import exit
import logging

logging.basicConfig(filename="main.log", format="%(asctime)s %(message)s", filemode="w")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
backendhandler = modules.datahandlers.backendhandler.DataHandler()

global screen
screen = curses.initscr()

# Server Data 
server_version = None
server_name = None

# Game Settings
# These don't work and soon they will be moved to another file
dont_show_button_prompts = False
auto_connect_to_server_ip = "example.com"
disable_logging = False

# Debug Switches
skip_ip = True
skip_new_save_file_message = True
skip_name_when_creating_new_save_files = True
skip_empire_name_when_creating_new_save_files = True


# Debug Options
debug_use_ip = "192.168.0.202:8000"
debug_create_save_file_with_name = "Test"
debug_create_save_file_with_empire_name = "Test"


# Global Functions

def quit_app():
  curses.endwin()
  exit()

def create_new_save_file_wizard():
  if not skip_new_save_file_message:
    screen.clear()
    screen.addstr(0,0, "Create a new save file")
    screen.addstr(1,0, "----------------------")
    screen.addstr(2,0, "You don't have a save file on this server so we will need to create")
    screen.addstr(3,0, "a new one, you will be asked to input the name of your character")
    screen.addstr(4,0, "and what you want to call your company, press any key to continue")
    screen.refresh()

    screen.get_wch()

  screen.clear()
  textbox = modules.uielements.textboxes.AlphaNumericTextBox(screen=screen)
  if not skip_name_when_creating_new_save_files:
    name = textbox.create_textbox("Your Name", (1,1), 16)
  else:
    name = debug_create_save_file_with_name
  if not skip_empire_name_when_creating_new_save_files:
    empire_name = textbox.create_textbox("Your Empire Name", (1,1), 16)
  else:
    empire_name = debug_create_save_file_with_empire_name

  if name == "QUIT" or empire_name == "QUIT":
    screen.clear()
    screen.addstr(0,0, "Error")
    screen.addstr(1,0, "-----")
    screen.addstr(2,0, "You cannot have a blank name or empire name, do you want to try again?")
    screen.addstr(3,0, "Press any key to retry")

    screen.get_wch()

    create_new_save_file_wizard()

  screen.clear()
  backendhandler.generate_save_file(name = name, empire_name=empire_name)
  return backendhandler.save_data

class Main():
  def __init__(self) -> None:
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0) 
    screen.keypad(True)
  
  def connect_to_server(self):
    if not skip_ip:
      ipaddress_textbox = modules.uielements.textboxes.AddressTextBox(screen=screen)

      ipaddress = ipaddress_textbox.create_textbox("Server Address", (1,1), 19)
      # screen.addstr(0,0,f"Function returned {ipaddress}")
      screen.refresh()
      if ipaddress == "QUIT":
        quit_app()
    else:
      ipaddress = debug_use_ip

    screen.clear()    
    screen.addstr(1,2, f"Connecting to {ipaddress}")
    screen.refresh()

    requesthandler.server_url = f"http://{ipaddress}"
    status = requesthandler.ping()

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
        screen.clear()
        requesthandler.server_url = None
        self.connect_to_server()
      else:
        quit_app()
    
  def retrieve_server_data(self):
    screen.clear()

    screen.addstr(0,0, "Loading")
    screen.addstr(1,0, "-------")
    screen.refresh()

    screen.addstr(3,1, "Getting Username (First run will take longer)")
    screen.addstr(4,1, "[-     ]")
    screen.refresh()

    requesthandler.username = usernamehandler.get_username()
    logger.debug(f'Username: {requesthandler.username}')
    
    screen.addstr(3,1, "Initializing Datahandlers (1/2)\t\t\t\t\t\t")
    screen.addstr(4,1, "[--    ]")
    screen.refresh()
    backendhandler.fill_arguments(server_url = requesthandler.server_url, username=requesthandler.username)
    backendhandler.fill_decryption_key_field()
    logger.debug(f'Backend Handler Filled Arguments: Server URL: {requesthandler.server_url}, Username: {requesthandler.username}\nDecryption Key: {backendhandler.key}, Cryptography Handler: {backendhandler.cryptographyhandler}')
  
    screen.addstr(3,1, "Initializing Datahandlers (2/2)\t\t\t")
    screen.addstr(4,1, "[---   ]")
    screen.refresh()
    datahandler.fill_property_data()
    logger.debug(f'Loading Stage 3: Called fill property data, property data={datahandler.properties}')


    screen.addstr(3,1, "Loading Save File\t\t\t\t")
    screen.addstr(4,1, "[----  ]")
    screen.refresh()
    logger.debug(f'Loading Stage 4: Parsing Save file')
    save_data = backendhandler.get_save_file()

    if save_data == "GENERATE":
      logger.warning("User doesn't have a save file on this server, creating new one")
      datahandler.save_data = create_new_save_file_wizard()
    else:
      datahandler.save_data = save_data

    datahandler.save_file_parser()
    
    screen.addstr(3,1, "Gathering Information (1/2)\t\t\t")
    screen.addstr(4,1, "[----- ]")
    screen.refresh()
    server_name = requesthandler.get_server_name()
    
    screen.addstr(3,1, "Gathering Information (2/2)")
    screen.addstr(4,1, "[------]")
    screen.refresh()
    server_version = requesthandler.get_server_version()

    # encrypted_save = self.requesthandler.cloudsave_get()
    # encrypted_save = encrypted_save.encode()

    # Handled by datahandler.get_save_file() function

    logger.info(f"Connected to {server_name} on version {server_version} on IP Address {requesthandler.server_url}")

    backendhandler.get_property_data()

    logger.debug(f"Property Data: {backendhandler.property_data}")
    screen.addstr(3,1, "Loading Game")
    screen.refresh()

    logger.debug("Loading User Interface")
    UserInterface()
    
class UserInterface:
  def __init__(self) -> None:
    self.Dashboard()
  
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

      # Render Row Titles
      screen.addstr(4, 0, "Business Statistics")
      screen.addstr(4, 25, "Property Management")

      screen.addstr(5,0, "-"*90)

      # Renders the business statistics

      # y, x
      screen.addstr(6, 2, f"Capital: {self.money}")
      screen.addstr(7, 2, f"Properties: {self.property_count}")


      # Renders property options

      screen.addstr(6, 25, "View [p]roperty Portfolio")
      screen.addstr(7, 25, "Visit the property [m]arket")

      # Renders other options

      screen.addstr(9, 0, "[H]elp\t[E]dit Business Documents\t[Q]uit")

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
      if key_press == 'q':
        UserInterface.BusinessIdentityManagement
      else:
        self.__init__()
  
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
  main.retrieve_server_data()

if __name__ == '__main__':
  main()