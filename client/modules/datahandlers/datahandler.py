import backendhandler

backendhandler = backendhandler.DataHandler()

# Please note that anything to do with changes during gameplay is handled
# in this module and not in the datahanlder (now backendhandler) module
# The DataHandler (now backendhandler) module deals with the backend.
# Please do remember that before creating useless functions

class DataHandler:

  save_data = backendhandler.save_data
  proprty_data = backendhandler.property_data

  # Parsed Save file Data goes here

  name, empire_name = None, None 
  money, properties, property_count = None, None, None

  def initialize(self, save_file):
    self.save_data = save_file

  def save_file_parser(self):
    self.name = self.save_data['name']
    self.empire_name = self.save_data['empire-name']
    self.money = self.save_data['money']
    self.properties = self.save_data['properties']
    self.property_count = len(self.properties)

  def save(self):
    def upload(self):
      backendhandler.save_data = self.save_data
      backendhandler.upload_savefile(backendhandler.encrypt_save_file(self.save_data))

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
  
  def change_empire_name(self, new_empire_name):
    self.empire_name = new_empire_name
    self.save()
  
  def handle_all_buy(self, property_name):
    # Get current property price
    property_values = self.proprty_data['property_name']
    property_cost = property_values['cost']

    # Remove Money
    self.money = self.money - property_cost

    # Add Property
    self.properties.append(property_name)

    # Save changes
    self.save()
  
  def handle_all_sell(self, property_name):
    # Get current property price
    property_values = self.proprty_data['property_name']
    property_cost = property_values['cost']

    # Add Money
    self.money = self.money + property_cost

    # Remove Property
    self.properties.remove(property_name)

    # Save changes
    self.save()