import requests
from cryptography.fernet import Fernet
import json

ENCRYPTOR = Fernet(b'jm3YewpnyOAnk-tyXNsN9mx0ZLYtnaASuKsaPoYNxhk=')

def load_property_data(server_address):
  print("Downloading property data")

  request = requests.get(f'http://{server_address}:8000/api/properties')
  property_data = request.json()
  
  return property_data