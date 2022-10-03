import requests
import os

import logging

# logging.basicConfig(filename="requesthandler.log", format="%(asctime)s %(message)s", filemode='w+')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class RequestHandler:

  server_url = ""
  username = ""
  data = ""

  def ping(self):
    try:
      requests.request("GET", f'{self.server_url}')
      return True
    except Exception:
      return "NO_CONNECTION"
    
  def query_data(self, query):
    # try:
    logger.debug(f"Server URL: {self.server_url}")
    response = requests.request("GET", f'{self.server_url}/{query}')
    return response
    # except Exception:
    #   return "NO_CONNECTION"
    
  def cloudsave_creator_deletor(self, request, username):

    headers = {"username": username}
    try:
      response = requests.request("{request}", f'{self.server_url}api/cloudsaves', headers=headers)
    except Exception:
      return "NO_CONNECTION"

    return response
  
  def delete_cloudsaves(self):

    res = self.cloudsave_creator_deletor("DELETE", self.username)
    if res == "NO_CONNECTION": return "NO_CONNECTION"
    return True
  
  def cloudsave_get(self):

    # res = self.cloudsave_creator_deletor("GET", self.username)

    headers = {"username": self.username}

    response = requests.request('GET', f'{self.server_url}/api/cloudsaves/', headers=headers)

    if response.status_code == 404: return "NOT_EXISTS"
    response = response.text.replace("\"", '')
    return response
  
  def update_cloudsaves(self):
    headers = {
    "username": self.username,
    "data": self.data
    }

    try:
      response = requests.request("PATCH", f'{self.server_url}api/cloudsaves', headers=headers)
      
      if response.status_code == 404:
        return "NOT_EXISTS"
       
      return response
    except Exception:
      return "NO_CONNECTION"
  
  def upload_cloudsaves(self):
    headers = {
    "username": self.username,
    "data": self.data
    }

    logger.debug(f"Headers sent to the server: {headers}")
    response = requests.request("PUT", f'{self.server_url}/api/cloudsaves/', headers=headers)
    return None

  def update_cloudsaves(self):
    headers = {
    "username": self.username,
    "data": self.data
    }
    try:
      response = requests.request("PATCH", f'{self.server_url}/api/cloudsaves/', headers=headers)
      if response.status_code == 404:
        return "NO_SAVE"
    except Exception:
      return "NO_CONNECTION"

  def get_decryption_key(self):
    logger.debug("Asked to get decryption key")
    key_request = self.query_data("api/server/key")
    key_request = key_request.text
    logger.debug(f"Decryption key from server: {key_request} ")
  
    if key_request == "NO_CONNECTION":
      return None

    key_request = key_request.replace("\"", "")
    return key_request.encode()
    
  def get_server_name(self):
    request = self.query_data('api/server/name')
    if request.text == "NO_CONNECTION": return "NO_CONNECTION"
    return request.text
    
  def get_property_data(self):
    request = self.query_data('api/properties')
    if request == "NO_CONNECTION": return "NO_CONNECTION"
    return request.text
    
  def get_server_version(self):
    request = self.query_data('api/server/version')
    if request.text == "NO_CONNECTION": return "NO_CONNECTION"
    return float(request.text)
