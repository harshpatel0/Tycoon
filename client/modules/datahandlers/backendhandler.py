import re
import cryptography
from cryptography.fernet import Fernet
from . import requesthandler

# requesthandler = requesthandler.RequestHandler()
requesthandler = requesthandler.RequestHandler()

# Please note that anything to do with changes during gameplay is handled
# in the inventoryhandler (now datahandler) module and not in the datahanlder
# (now backendhandler) module. The DataHandler (now backendhandler) module 
# deals with the backend. Please do remember that before creating useless functions

class DataHandler:

  save_data = None
  property_data = None
  key, cryptographyhandler = None, None

  # This function is used because you first need to connect to the server to receive the data
  def fill_decryption_key_field(self):
    self.key = requesthandler.get_decryption_key()
    self.cryptographyhandler = Fernet(self.key)

  def fill_arguments(self, server_url, username, data = None):
    requesthandler.server_url = server_url
    requesthandler.username = username
    requesthandler.data = data

    return None

  def get_save_file(self):
    save_file = requesthandler.cloudsave_get()
    return save_file

  def decrypt_encrypted_save(self, encrypted_save_file):
    
    encrypted_save_file = self.get_save_file()
  
    try:
      self.save_data = self.cryptographyhandler.decrypt(encrypted_save_file)
    except cryptography.fernet.InvalidToken:
      return "INCORRECT KEY"
    return self.save_data
  
  def encrypt_save_file(self):
    return self.cryptographyhandler.encrypt(self.save_data)
  
  def save_user_data(self, data):
    self.save_data = data
  
  def get_property_data(self):
    if self.property_data == None:
      self.property_data = requesthandler.get_property_data()
    return self.property_data
  
  def get_save_file(self):
    request_to_server = requesthandler.cloudsave_get()
    if request_to_server.text == "NOTFOUND":
      self.generate_save_file()
      return "GENERATE"

    else:
      if self.decrypt_encrypted_save(request_to_server.text.encode()) == "INCORRECT KEY":
        return "INCORRECT KEY"
      return self.save_data
  
  def upload_savefile(self, encrypted_save_file):
    requesthandler.data = encrypted_save_file
    requesthandler.upload_cloudsaves()  
    return None
  
  def generate_save_file(self, name, empire_name):

    starting_cash = 10000

    save_file = {
      "name": name,
      "empire-name": empire_name,
      "money": starting_cash,
      "properties": []
    }

    self.save_data = save_file

    self.upload_savefile(self.encrypt_save_file())