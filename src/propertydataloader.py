import requests
from cryptography.fernet import Fernet
import json

ENCRYPTOR = Fernet(b'jm3YewpnyOAnk-tyXNsN9mx0ZLYtnaASuKsaPoYNxhk=')

def download_property_data(server_address):
  print("Downloading property data")

  request = requests.get(f'http://{server_address}:5000/api/properties')
  property_data = request.json()

  print("Encrypting Property Data")

  storing_property_data = json.dumps(property_data).encode('utf-8')

  encrypted_property_data = ENCRYPTOR.encrypt(storing_property_data)

  print("Saving Property Data")
  with open('properties.dat', 'wb') as property_data_file:
    property_data_file.write(encrypted_property_data)
  
  return property_data

def load_local_property_data():
    print("Loading saved property data")

    try:
      with open('properties.dat', 'rb') as property_data_file:
        property_data = property_data_file.read()
    except FileNotFoundError:
      print('''
      A local copy of the properties data file was not found, to download a properties
      folder connect to a server, it should automatically download when you connect to the 
      server
      ''')
    
    print("Decrypting Property Data")
    property_data = ENCRYPTOR.decrypt(property_data)
    property_data = json.loads(property_data.decode('utf-8'))

    return property_data