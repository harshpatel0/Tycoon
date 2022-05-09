from . import backendhandler
import logging

backendhandler = backendhandler.DataHandler()

# Please note that anything to do with changes during gameplay is handled
# in this module and not in the datahanlder (now backendhandler) module
# The DataHandler (now backendhandler) module deals with the backend.
# Please do remember that before creating useless functions

# Intialize Logger
# logging.basicConfig(filename="backendhandler.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class DataHandler:

  save_data = None
  property_data = None

  cryptographyhander = None

  # Parsed Save file Data goes here

  name, empire_name = None, None 
  money, properties, property_count = None, None, None
  property_data = None
  
  def fill_property_data(self):
    self.property_data = backendhandler.get_property_data()

  def save_file_parser(self):
    self.name = self.save_data['name']
    self.empire_name = self.save_data['empire-name']
    self.money = self.save_data['money']
    self.properties = self.save_data['properties']
    self.property_count = len(self.properties)

  def save(self, cryptographyhandler):
    def upload():
      backendhandler.save_data = self.save_data
      # backendhandler.upload_savefile(backendhandler.encrypt_save_file(self.save_data))
      encrypted_save_file = backendhandler.encrypt_save_file_for_saving(cryptographyhandler)
      logger.debug(f"Encrypted save file to send: {encrypted_save_file}")
      backendhandler.upload_savefile(encrypted_save_file)

    self.save_data['name'] = self.name
    self.save_data['empire-name'] = self.empire_name
    self.save_data['money'] = self.money
    self.save_data['properties'] = self.properties

    upload()
    self.save_file_parser()

    return "SUCCESS"

  def remove_money(self, amount):
    self.money = self.money - amount
    self.save()
  
  def add_money(self, amount):
    self.money = self.money + amount
    self.save()
  
  def add_property(self, property_name):
    self.properties.append(property_name)
    self.save()
  
  def remove_property(self, property_name):
    self.properties.remove(property_name)
    self.save()

  def change_name(self, new_name):
    self.name = new_name
    self.save()
  
  def change_empire_name(self, new_name):
    self.empire_name = new_name
    self.save()

  def check_buy_requirements(self, property_name, price):

    temp_money = int(self.money) - int(price)

    # This is a useless step, just for the fun of it
    if property_name in self.properties and temp_money < 0:
      return "SHAMBLES"

    # Check if the property is already bought
    if property_name in self.properties:
      return "ALREADY PURCHASED"
    
    # Check if they have enough money
    if temp_money < 0:
      return "NO FUNDS"

    return "SUCCESS"

  def check_sell_requirements(self, property_name):
    # Check if the property is already bought
    if property_name not in self.properties:
      return "NOT OWNED"

    return "SUCCESS"

  def handle_all_sell(self, property_name):
    # Get current property price
    property_values = self.property_data[property_name]
    property_cost = property_values['cost']

    # Check if it can be bought
    result = self.check_buy_requirements(property_name = property_name, price = property_cost)

    expected_results = ["SHAMBLES", "ALREADY PURCHASED", "NO FUNDS"]
    if result in expected_results: return result

    # Remove Money
    self.money = int(self.money) - int(property_cost)

    # Add Property
    self.properties.append(property_name)

    # Save changes
    logger.debug(f"Cryptography Handler {self.cryptographyhander}")
    self.save(self.cryptographyhander)

    return "SUCCESS"
  
  def handle_all_sell(self, property_name):
    # Get current property price
    property_values = self.property_data[property_name]
    property_cost = property_values['cost']

    # Check Sell Requirements
    result = self.check_sell_requirements(property_name=property_name)
    if result == "NOT OWNED": return result

    # Add Money
    self.money = int(self.money) + int(property_cost)

    # Remove Property
    self.properties.remove(property_name)

    # Save changes
    logger.debug(f"Cryptography Handler {self.cryptographyhander}")
    self.save(self.cryptographyhander)

    return "SUCCESS"
