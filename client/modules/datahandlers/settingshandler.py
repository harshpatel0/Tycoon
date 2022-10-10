import json
import logging

logger = logging.getLogger()

class SettingsHandler:
  def load_settings(self, file_path:str = 'settings.json'):
    with open(f'{file_path}', 'r') as settingsfile:
      logger.info(f"Loading settings file in {file_path}")
      self.raw_settings = json.load(settingsfile)
      logger.debug(f"Loaded setting data {self.raw_settings}")
    
  def parse_settings(self):
    logger.info("Parsing raw setting data")
    # Parse all setting subgroups
    connection_settings = self.raw_settings['connection_settings']
    userinterface_settings = self.raw_settings['userinterface_settings']
    keybindings = self.raw_settings['keybindings']
    flags = self.raw_settings['flags'] # This setting subgroup does not need to be parsed further
    
    logger.debug(f"""
    Parsed Setting Subgroups
    -------------------------
    Connection Settings:      {connection_settings}
    User Interface Settings:  {userinterface_settings}
    Keybindings:              {keybindings}
    Flags:                    {flags
    }""")

    # Parse Connection Settings
    self.enable_autoconnect = connection_settings['enable_autoconnect']
    self.autoconnect_to_server_address = connection_settings['autoconnect_to_server_address']

    # Parse Userinterface Settings
    self.show_button_prompts = userinterface_settings['show_button_prompts']

    # Parse Keybindings
    self.action_key = keybindings['action_key']
    self.quit_userinterface_key = keybindings['quit_userinterface']
    self.backspace_key = keybindings['backspace']
    self.accept_key = keybindings['accept_key']
    self.quit_key = keybindings['quit_key']

  def change_setting_value(self, setting, new_value):
    """
    This method presumes that all the necessary checks have been done and that the data
    is good to be saved. Please ensure that checks are implemented correctly to avoid weird
    edge cases
    """
    logger.debug(f"Changing {setting} from {self.raw_settings[setting]} to {new_value}")
    self.raw_settings[setting] = new_value
