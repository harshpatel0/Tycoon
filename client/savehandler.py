import requesthandler
from cryptography.fernet import Fernet

requesthandler = requesthandler.RequestHandler()

class SaveHandler:

  key = requesthandler.get_decryption_key()

  save_data = None
  cryptographyhandler = Fernet(key)

  def fill_data(self, server_url, username, data):
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
  
  def save_data(self, data):
    self.save_data = data