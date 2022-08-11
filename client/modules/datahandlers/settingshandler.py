import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

settings_layout = {
  "enable_logging": {
    "name": "Enable Logging",
    "description": "Allows the client to log unsensitive information\nInformation such as keys or user data won't be recorded",
    "category": "Debug",
    "type": "boolean"},

  "enable_autoconnect": {
    "name": "Enable Autoconnect",
    "description": "Automatically connects to a specific server address",
    "category": "Connections",
    "type": "boolean"},

  "auto_connect_to_server": {
    "name": "Auto Connect to Server Address",
    "description": "What server address the client will automatically try to connect to",
    "category": "Connections",
    "type": "string"},

  "enable_button_tooltips": {
    "name": "Enable Button Tooltips/Prompts",
    "description": "Shows what buttons should be pressed in each menu, added due to button mapping inconsistencies",
    "category": "User Experiences / User Interface",
    "type": "boolean"},

  "enable_experimental_settings": {
    "name": "Enable Experimental Settings",
    "description": "Enables features that are still being worked on",
    "category": "Debug",
    "type": "boolean"}
}

defaults = {
  "enable_logging": False,
  "enable_autoconnect": False,
  "auto_connect_to_server": "",
  "enable_button_tooltips": True,
  "enable_experimental_settings": False
}

class SettingsHandler:

  raw = None
  file_path = None

  enable_logging = None
  
  enable_autoconnect = None
  auto_connect_to_server = None 
  
  enable_button_tooltips = None

  def __init__(self, file_path) -> None:
    self.file_path = file_path

    logger.debug("Attempting to load settings")
    self.load_settings(file_path)

  def generate_new_settings_file(self):
    self.save_file(defaults, self.file_path) 

  def load_settings(self, file_path):
    try:
      with open(file_path, 'r') as settings_file:
        self.raw = json.load(settings_file)
    except FileNotFoundError:
      logger.debug("Handled Exception: FileNotFoundError, generating new settings file and retrying load")
      self.generate_new_settings_file()
      self.load_settings()

    self.set_settings(self.raw)
  
  def set_settings(self, settings):
    self.enable_logging = settings["enable_logging"]
    
    self.enable_autoconnect = settings["enable_autoconnect"]
    self.auto_connect_to_server = settings["auto_connect_to_server"]

    self.enable_button_tooltips = settings['enable_button_tooltips']

  def change_settings(self, setting, new_value):
    self.raw[setting] = new_value
  
  def save_file(self, raw_data, file_path):
    with open(file_path, 'w') as settings_file:
      json.dump(settings_file, raw_data)
  
class SettingsUI():
  screen = None
  raw_settings = None

  # Data Gatherer Properties
  page = 0

  def __init__(self, screen, raw_settings) -> None:
    self.screen = screen
    self.raw_settings = raw_settings
  
  def data_gatherer(self):
    key_list = tuple(settings_layout.keys())

    try:
      data = self.properties[key_list[self.page]]
    except IndexError:
      self.page = 0
      data = self.properties[key_list[self.page]]
    
      logger.debug(f"Settings Manager: Loaded Settings Layout data {data}")
    
    # Assemble Data into List
    page = self.page
    name = data["name"]
    description = data["description"]
    category = data["category"]
    type = data["type"]

    current_value = self.raw_settings[key_list[self.page]]

    details = (page, name, description, category, current_value)
    self.render(type, details=details)

  def render(self, type, details):
    # Unpack List
    page = details[0]
    name = details[1]
    description = details[2]
    category = details[3]
    current_value = details[4]


    self.screen.clear()
                      # y, x
    self.screen.addstr(0,0, "Settings Manager")
    self.screen.addstr(1, 0, f"{page}/{len(settings_layout)}")
    self.screen.addstr(2, 0, f"{category} -> {name}")
    self.screen.addstr(3, 1, f"{description}")

    self.screen.addstr(5, 0, f"Currently set to {current_value}")
    
    # Here is where the setting changer will be located