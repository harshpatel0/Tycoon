import requesthandler
from cryptography.fernet import Fernet

requesthandler = requesthandler.RequestHandler()

class DataHandler:

  key = requesthandler.get_decryption_key()

  save_data = None
  cryptographyhandler = Fernet(key)

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
  
    self.save_data = self.cryptographyhandler.decrypt(encrypted_save_file)
    return self.save_data
  
  def encrypt_save_file(self):
    return self.cryptographyhandler.encrypt(self.save_data)
  
  def save_user_data(self, data):
    self.save_data = data
  
  def get_property_data(self):
    return requesthandler.get_property_data()
  
  def upload_savefile(self, encrypted_save_file):
    requesthandler.data = encrypted_save_file
    requesthandler.upload_cloudsaves()  
    return None
  
  def generate_save_file(self, name, empire_name):

    starting_cash = 10000

    save_file = {
      "name": name,
      "empire-name": empire_name,
      "money": starting_cash
    }

    self.save_data = save_file

    self.upload_savefile(self.encrypt_save_file())