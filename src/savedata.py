from cryptography.fernet import Fernet
from datetime import date
import json
import requests

# This key is used to encrypt and decrypt save and profile files
KEY = b'jm3YewpnyOAnk-tyXNsN9mx0ZLYtnaASuKsaPoYNxhk='

def get_key():
  pass

def cloudsave(address, uuid):
  print("Requesting cloud save from the server")

  request = requests.get(f"http://{address}:5000/api/cloudsave/?uuid={uuid}")
  save_data = request.text

  if save_data == 'BADRESPONSE':
    return 'FAILED'
  if save_data == 'NOTFOUND':
    return 'NOTFOUND'

  print("Decrypting cloud save")

  ENCRYPTOR = Fernet(KEY)

  save_data = save_data.encode('utf-8')
  
  decrypted_save = ENCRYPTOR.decrypt(save_data)
  decrypted_save = json.loads(decrypted_save.decode('utf-8'))

  save_data = save_data.decode('utf-8')
  print("Saving save file")
  game_data = json.dumps(save_data).encode('utf-8')

  output = ENCRYPTOR.encrypt(game_data)

  with open('data.sav', 'wb') as game_data:
    game_data.write(output)
    
  return decrypted_save

def create_save():
  profile_name = input("Type a name for your profile: ")
  empire_name = input("Type a name for your empire: ")

  game_data = {
    "profileName": profile_name,
    "empireName": empire_name,
    "capital": 10000,
    "ownedBusinesses": 0,
    "businesses": []
  }

  enocoded_game_data = json.dumps(game_data).encode('utf-8')
  
  ENCRYPTOR = Fernet(KEY)
  output = ENCRYPTOR.encrypt(enocoded_game_data)

  with open('data.sav', 'wb') as game_data:
    game_data.write(output)
  
  return game_data

def save_game_save(data):
  game_data = json.dumps(data).encode('utf-8')
  
  ENCRYPTOR = Fernet(KEY)
  output = ENCRYPTOR.encrypt(game_data)

  with open('data.sav', 'wb') as game_data:
    game_data.write(output)
  
def load_save():
  with open('data.sav', 'rb') as game_data:
    save_data = game_data.read()
  
  ENCRYPTOR = Fernet(KEY)
  
  decrypted_save = ENCRYPTOR.decrypt(save_data)
  decrypted_save = json.loads(decrypted_save.decode('utf-8'))

  return decrypted_save

def check_save():
  # Checks if the file exists or not, ik this is a really really really shit way of doing this
  # but I couldn't care less, optimizing code is for nerds not for us elite chad programmers
  try:
    this_is_a_shit_way_of_doing_things = open('game.sav')
    this_is_a_shit_way_of_doing_things.close()

    return 'SAVEEXISTS'
  except IOError:
    return 'NOSAVEFOUND'
