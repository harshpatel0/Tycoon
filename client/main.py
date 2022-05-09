print("Loading Files")
import curses
from sys import exit
import logging

from idna import valid_contextj

# from time import sleep

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
debug_skip_ip = True
debug_skip_new_save_file_message = True
debug_skip_name_when_creating_new_save_files = True
debug_skip_empire_name_when_creating_new_save_files = True
debug_enable_wip_features = True
debug_ignore_settings_file = False # Unused


# Debug Options
debug_use_ip = "192.168.0.105:8000"
debug_create_save_file_with_name = "Test"
debug_create_save_file_with_empire_name = "Test"


# Global Functions

def quit_app():
  curses.endwin()
  exit()

def create_new_save_file_wizard():
  if not debug_skip_new_save_file_message:
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
  if not debug_skip_name_when_creating_new_save_files:
    name = textbox.create_textbox("Your Name", (1,1), 16)
  else:
    name = debug_create_save_file_with_name
  if not debug_skip_empire_name_when_creating_new_save_files:
    empire_name = textbox.create_textbox("Your Empire Name", (1,1), 16)
  else:
    empire_name = debug_create_save_file_with_empire_name

  if name == "QUIT" or empire_name == "QUIT":
    screen.clear()
    screen.addstr(0,0, "Error")
    screen.addstr(1,0, "-----")
    screen.addstr(2,0, "You cannot have a blank name or empire name, do you want to try again?")
    screen.addstr(3,0, "Press any key to retry or press q to quit app")

    keypress = screen.get_wch()

    if keypress == "q":
      exit()

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
    if not debug_skip_ip:
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
    
    datahandler.cryptographyhander = backendhandler.cryptographyhandler
    logger.debug("Passed cryptography handler to DataHandler")
  
    screen.addstr(3,1, "Initializing Datahandlers (2/2)\t\t\t")
    screen.addstr(4,1, "[---   ]")
    screen.refresh()
    datahandler.fill_property_data()
    logger.debug(f'Loading Stage 3: Called fill property data, property data={datahandler.property_data}')


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
      screen.addstr(4, 30, "Property Management")

      screen.addstr(5,0, "-"*90)

      # Renders the business statistics

      # y, x
      screen.addstr(6, 2, f"Capital: TY$ {self.money}")
      screen.addstr(7, 2, f"Properties: {self.property_count}")


      # Renders property options

      screen.addstr(6, 30, "View [p]roperty Portfolio")
      screen.addstr(7, 30, "Visit the property [m]arket")

      # Renders other options

      if not dont_show_button_prompts:
        screen.addstr(9, 0, "[H]elp\t[E]dit Business Documents\t[Q]uit")

      screen.refresh()
    
    def handle_keypress(self):
      key_press = screen.get_wch()

      if key_press == 'p':
        logger.info("Loading Property Portfolio")
        UserInterface.PropertyPortfolio()
      if key_press == 'm':
        logger.info("Loading Property Market")
        UserInterface.PropertyMarket()
      if key_press == 'h':
        logger.info("Loading Game Help")
        UserInterface.GameHelp()
      if key_press == 'e':
        logger.info("Loading Business Identity Management")
        UserInterface.BusinessIdentityManagement()
      if key_press == 'q':
        logger.info("Quitting app")
        logger.debug(f"Cryptography Handler in Dashboard: {backendhandler.cryptographyhandler}")
        datahandler.save(backendhandler.cryptographyhandler)
        exit()
      else:
        self.__init__()
  
  class PropertyPortfolio:

    page = 0
    properties, property_count = None, None
    property_data = None
    money = None
    
    def __init__(self) -> None:
      screen.clear()
      self.properties = datahandler.properties
      self.property_count = datahandler.property_count
      self.property_data = datahandler.property_data
      self.money = datahandler.money
      logger.debug(f'Properties in save file: {self.properties}')
      self.data_gatherer()
    
    def render_dialog(self,message):
      screen.clear()
                  # y,x 
      screen.addstr(0,0, f"[Q]uit\t\tAlert")        
      screen.addstr(1,0, "---------------------------------")

      if message == "NO PROPERTIES":
        screen.addstr(2,0, "You don't own any properties")
        screen.addstr(3,0, "Visit the property market to buy properties, if you think this is an error report the problem")
        screen.addstr(4,0, "Visit the report a problem guide on the website before reporting a problem")
        screen.addstr(5,0, "Error Code: NO PROPERTIES")
      if message == "NOT OWNED":
        screen.addstr(2,0, "You don't own this property")
        screen.addstr(3,0, "It seems like you don't own this property")
        screen.addstr(4,0, "This is definately an issue and should be reported")
        screen.addstr(5,0, "Error Code: NOT OWNED")
      else:
        screen.addstr(2,0, "Successfully sold")
        screen.addstr(3,0, f"This property has been sold, you now have TY$ {datahandler.money}")
        self.money = datahandler.money

      screen.addstr(5,0, "Press ANY KEY to go back to the dashboard")
      screen.refresh()

      screen.get_wch()
      screen.clear()
      return None

    def data_gatherer(self):
      if self.property_count == 0:
        self.render_dialogs("NO PROPERTIES")
        UserInterface.Dashboard()

      value_pairs = self.properties

      # Use the value pairs to get the property details from the property data
      try:
        property_info_for_property = self.property_data[value_pairs[self.page]]
      except IndexError:
        self.page = self.property_count
        property_info_for_property = self.property_data[value_pairs[self.page]]

      logger.debug(f'Property Information for the Property {self.page} of owned properties {property_info_for_property}')

      name = value_pairs[self.page]
      location = property_info_for_property['location']
      cost = property_info_for_property['cost']
      set = property_info_for_property['set']

      page = self.page + 1
      max_page = self.property_count

      logger.debug(f'Name: {name}, Cost: {cost}, Location: {location}, Set: {set}, Max Page: {max_page}')

      self.render(page, name, cost, location, set, max_page)
      # UserInterface.Dashboard()
    
    def handle_selling(self, name):
      # Handle all the outputs of buying properties
      output_of_sell = datahandler.handle_all_sell(name)
      self.render_dialog(output_of_sell)
      return None

    def render(self, page: int, name: str, selling_price: int, location: str, set: str, max_page: str):
      screen.clear()
                    # y,x 
      screen.addstr(0,0, f"[Q]uit\t\tProperty Market\t\tYou have TY$ {self.money}")        
      screen.addstr(1,0, "------------------------------------------------------------------------")
      screen.addstr(2,0, f"Page: {page}/{max_page}")
      screen.addstr(4,0, f"{name}")
      screen.addstr(5,0, f'Price: TY$ {selling_price}')
      screen.addstr(6,0, f'Located in: {location}\tPart of {set} set')

      # Key help

      def determine_nav_key():
        if page == 1:
          return "[->]Next Page"
        if page == max_page:
          return "[<-]Previous Page"
        if page != 1 and page != max_page:
          return "[<-]Previous Page\t[->]Next Page"

      screen.addstr(7,0, len(f'Located in: {location}\tPart of {set} set') * '-' + (7 * '-'))
      screen.addstr(8,0, f"Sell [SPACE]\t{determine_nav_key()}\t[Q]uit")

      keypress_output = self.handle_keypress()

      if keypress_output == "SELL":
        self.handle_selling(name)

    def handle_keypress(self):
      # Keys
      next_key = 261
      previous_key = 260
      action_key = ' '
      quit_key = 'q'

      key_press = screen.get_wch()
      logger.debug(f"Pressed {key_press}")

      if key_press == next_key:
        logger.debug(f"Next Page")
        self.page = self.page + 1
        self.data_gatherer()
        
      if key_press == previous_key:
        logger.debug(f"Previous Page")
        if self.page != 0:
          self.page = self.page - 1
          self.data_gatherer()
        else:
          self.handle_keypress()
        
      if key_press == quit_key:
        logger.debug(f"Quit Key")
        UserInterface.Dashboard()
        
      if key_press == action_key:
        logger.debug(f"Sell Key")
        return "SELL"

  class PropertyMarket:
    money, property_count = None, None
    
    # This will be used to see which property to load and what property the user has chosen to bought
    page = 0
  
    # Property Data
    properties = {}

    def __init__(self) -> None:
      screen.clear()
      self.init_data()
      # self.render() # Special case
      logger.debug(f"Property Market Variables: Money: {self.money} Page: {self.page} Properties: {self.properties}")
      logger.debug(f'Property Data in DataHandler() {datahandler.property_data}')

      self.properties = datahandler.property_data

      self.data_gatherer()
      # self.handle_keypress() # Handled in render funcyion

    def init_data(self):
      self.money = datahandler.money
      self.property_count = datahandler.property_count
    
    def data_gatherer(self):
      # First get the keys
      key_list = tuple(self.properties.keys())

      logger.debug(f'Property Keys: {key_list}, Page: {self.page}')
      # Then get the one we want to get
      try:
        data = self.properties[key_list[self.page]]
      except IndexError:
        # Here the page variable has passed higher than what the list actually has
        self.page = len(key_list) - 1
        data = self.properties[key_list[self.page]]

      # Data is assembled here before sending
      page = self.page
      name = key_list[self.page]
      cost = data['cost']
      location = data['location']
      set = data['set']
      max_page = len(key_list)
      page = self.page + 1

      logger.debug(f'Name: {name}, Cost: {cost}, Location: {location}, Set: {set}, Max Page: {max_page}')

      self.render(page, name, cost, location, set, max_page)
    
    def handle_buying(self, name):
      # Handle all the outputs of buying properties
      output_of_buy = datahandler.handle_all_sell(name)
      self.render_dialog(output_of_buy)
      return None

    def render(self, page: int, name: str, cost: int, location: str, set: str, max_page: str):
      screen.clear()
                    # y,x 
      screen.addstr(0,0, f"[Q]uit\t\tProperty Market\t\tYou have TY$ {self.money}")        
      screen.addstr(1,0, "------------------------------------------------------------------------")
      screen.addstr(2,0, f"Page: {page}/{max_page}")
      screen.addstr(4,0, f"{name}")
      screen.addstr(5,0, f'Price: TY$ {cost}')
      screen.addstr(6,0, f'Located in: {location}\tPart of {set} set')

      # Key help

      def determine_nav_key():
        if page == 1:
          return "[->]Next Page"
        if page == max_page:
          return "[<-]Previous Page"
        if page != 1 and page != max_page:
          return "[<-]Previous Page\t[->]Next Page"

      screen.addstr(7,0, len(f'Located in: {location}\tPart of {set} set') * '-' + (7 * '-'))
      screen.addstr(8,0, f"Buy [SPACE]\t{determine_nav_key()}\t[Q]uit")

      keypress_output = self.handle_keypress()

      if keypress_output == "BUY":
        self.handle_buying(name)

    def handle_keypress(self):
      # Keys
      next_key = 261
      previous_key = 260
      action_key = ' '
      quit_key = 'q'

      key_press = screen.get_wch()
      logger.debug(f"Pressed {key_press}")

      if key_press == next_key:
        logger.debug(f"Next Page")
        self.page = self.page + 1
        self.data_gatherer()
        
      if key_press == previous_key:
        logger.debug(f"Previous Page")
        if self.page != 0:
          self.page = self.page - 1
          self.data_gatherer()
        else:
          self.handle_keypress()
        
      if key_press == quit_key:
        logger.debug(f"Quit Key")
        UserInterface.Dashboard()
        
      if key_press == action_key:
        logger.debug(f"Buy Key")
        return "BUY"

    def render_dialog(self, message):
      screen.clear()
                  # y,x 
      screen.addstr(0,0, f"[Q]uit\t\tAlert\t\tYou have TY$ {self.money}")        
      screen.addstr(1,0, "---------------------------------")
      if message == "SHAMBLES":
        screen.addstr(2,0, "You already own this property")
        screen.addstr(3,0, "And it isn't like you have money to buy it even if you didn't have it")
        screen.addstr(4,0, "Error Code: SHAMBLES")
      if message == "ALREADY PURCHASED":
        screen.addstr(2,0, "You already own this property")
        screen.addstr(4,0, "Error Code: ALREADY PURCHASED")
      if message == "NO FUNDS":
        screen.addstr(2,0, "You don't have enough money to buy this property")
        screen.addstr(4,0, "Error Code: NO FUNDS")
      else:
        screen.addstr(2,0, "The property was successfully bought")
        screen.addstr(3,0, f"You now have $TY {datahandler.money}")
      screen.addstr(6,0, "Type any key to go back")

      screen.refresh()

      screen.get_wch()
      screen.clear()
      return None

    def handle_buyinh(self, name):
      # Handle all the outputs of buying properties
      output_of_buy = datahandler.handle_all_sell(name)
      self.render_dialog(output_of_buy)
      return None
    
    def render(self, page: int, name: str, cost: int, location: str, set: str, max_page: str):
      screen.clear()
                  # y,x 
      screen.addstr(0,0, f"[Q]uit\t\tProperty Market\t\tYou have TY$ {self.money}")        
      screen.addstr(1,0, "---------------------------------")
      screen.addstr(2,0, f"Page: {page}/{max_page}")
      screen.addstr(4,0, f"{name}")
      screen.addstr(5,0, f'TY$ {cost}')
      screen.addstr(6,0, f'Located in: {location}\tPart of {set} set')

      # Key help

      def determine_nav_key():
        if page == 1:
          return "[->]Next Page"
        if page == max_page:
          return "[<-]Previous Page"
        if page != 1 and page != max_page:
          return "[<-]Previous Page\t[->]Next Page"

      screen.addstr(7,0, len(f'Located in: {location}\tPart of {set} set') * '-' + (7 * '-'))
      screen.addstr(8,0, f"Buy [SPACE]\t{determine_nav_key()}\t[Q]uit")

      keypress_output = self.handle_keypress()
      if keypress_output == "BUY":
        self.handle_buyinh(name)

    def handle_keypress(self):
      # Keys
      next_key = 261
      previous_key = 260
      buy_key = ' '
      quit_key = 'q'

      key_press = screen.get_wch()
      logger.debug(f"Pressed {key_press}")

      if key_press == next_key:
        logger.debug(f"Next Page")
        self.page = self.page + 1
        self.data_gatherer()
      
      if key_press == previous_key:
        logger.debug(f"Previous Page")
        if self.page != 0:
          self.page = self.page - 1
          self.data_gatherer()
        else:
          self.handle_keypress()
      
      if key_press == quit_key:
        logger.debug(f"Quit Key")
        UserInterface.Dashboard()
      
      if key_press == buy_key:
        logger.debug(f"Buy Key")
        return "BUY"

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