import re
import cryptography
from cryptography.fernet import Fernet
from . import requesthandler
import logging

# Used to convert strings to dictionaries
import json
                  
# Intialize Logger
logging.basicConfig(filename="backendhandler.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
    logger.debug('Executed fill_decryption_key_field')
    self.key = requesthandler.get_decryption_key()
    logger.debug(f'Got decryption key, Key: {self.key}')
    self.cryptographyhandler = Fernet(self.key)
    logger.debug('Initialized cryptography module')

  def fill_arguments(self, server_url, username, save_data = None):
    requesthandler.server_url = server_url
    requesthandler.username = username
    requesthandler.save_data = save_data

    return None

  # def get_save_file(self):
  #   save_file = requesthandler.cloudsave_get()
  #   return save_file

  def convert_to_dictionary(self, data, name_of_data = None):
    # name_of_data is used for logging
    logger.debug(f"Inital data before converting to dictionary: {data}, Name of data: {name_of_data}")
    
    data = data.replace('\'', '\"')
    logger.debug(f"After double quotting: {data}, Name of data: {name_of_data}")

    data = json.loads(data)
    logger.debug(f"JSON Module Output of Save File: {data}, Name of data: {name_of_data}")

    return data

  def decrypt_encrypted_save(self, encrypted_save_file):
    # encrypted_save_file = self.get_save_file()
    try:
      self.save_data = self.cryptographyhandler.decrypt(encrypted_save_file)
      logger.debug(f"Decrypted save file: {self.save_data}")

    except cryptography.fernet.InvalidToken:
      return "INCORRECT KEY"
    
    # Try to decode the save file before returning it as a dictionary
    self.save_data = self.save_data.decode()
    self.save_data = self.convert_to_dictionary(self.save_data, "Save File")

    return self.save_data
  
  def encrypt_save_file(self):
    logger.debug(f"Save file: {self.save_data}")

    # The save data first has to be encoded because of the cryptography module
    encrypted_save_file = self.cryptographyhandler.encrypt(str(self.save_data).encode())
    logger.debug(f"Encrypted Save File: {encrypted_save_file}")
    return encrypted_save_file

  def save_user_data(self, data):
    self.save_data = data
  
  def get_property_data(self):
    if self.property_data == None:
      self.property_data = requesthandler.get_property_data()
    
    # Needs to be made into a dictionary first
    self.property_data = self.convert_to_dictionary(self.property_data, "Property Data")
    return self.property_data
  
  def get_save_file(self):
    request_to_server = requesthandler.cloudsave_get()
    if request_to_server == "NOT_EXISTS":
      return "GENERATE"
      # self.generate_save_file()
    else:
      logger.debug(f"Save File From Server: {request_to_server}")
      encoded_request = request_to_server.encode()
      logger.debug(f"Encoded Save File: {encoded_request}")


      if self.decrypt_encrypted_save(encoded_request) == "INCORRECT KEY":
        return "INCORRECT KEY"
      return self.save_data
  
  def upload_savefile(self, encrypted_save_file):
    logger.info("Uploading save file to server")
    requesthandler.data = encrypted_save_file
    logger.debug(f"Request Handler > Data: {requesthandler.data}")
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