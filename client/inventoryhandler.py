import datahandler

datahandler = datahandler.DataHandler()

class InventoryHandler:

  save_data = datahandler.save_data

  # Parsed Save file Data goes here

  name, empireName = None, None 
  cash, properties = None, None

  def initialize(self, save_file):
    self.save_data = save_file

  def save_file_parser(self):
    self.name = self.save_data['name']
    self.empireName = self.save_data['empire-name']
    self.cash = self.save_data['cash']
    self.properties = self.save_data['properties']
  
  def upload(self):
    datahandler.save_data = self.save_data
    datahandler.upload_savefile(datahandler.encrypt_save_file(self.save_data))

  def save(self):
    self.save_data['name'] = self.name
    self.save_data['empire-name'] = self.empireName
    self.save_data['cash'] = self.cash
    self.save_data['properties'] = self.properties

    self.upload()

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
