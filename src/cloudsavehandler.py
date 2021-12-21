from cryptography.fernet import Fernet
from requesthandlers import RequestHandler
from usernamehandler import UsernameHandler
import json

requesthandler = RequestHandler()
usernamehandler = UsernameHandler()

class CreateSaves():
  username = usernamehandler.get_username()

  def upload_save_file(self, encrypted_save_file):
    requesthandler.upload_cloudsaves(self.username, encrypted_save_file)

  def generate_save_file(self, profile_name, empire_name):
    game_data = {
      "profileName": profile_name,
      "empireName": empire_name,
      "capital": 10000,
      "ownedBusinesses": 0,
      "businesses": []
    }

    enocoded_game_data = json.dumps(game_data).encode('utf-8')
    
    key = requesthandler.get_key()
    key = key.encode()

    ENCRYPTOR = Fernet(key)
    output = ENCRYPTOR.encrypt(enocoded_game_data)
    return output

class DecryptSaves():
  key = b""
  encryptor = None

  def __init__(self) -> None:
    temp_key = requesthandler.get_key()

    self.key = temp_key.encode()
    self.encryptor = Fernet(self.key)
  
  def get_details_for_decryption(self):
    return usernamehandler.get_username()

  def decrypt_saves(self, encrypted_save_file):
    encrypted_save_file = requesthandler.get_cloudsaves(username = self.get_details_for_decryption())
    return self.encryptor.decrypt(encrypted_save_file)