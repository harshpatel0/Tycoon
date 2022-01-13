import requests

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
    try:
      response = requests.request("GET", f'{self.server_url}/{query}')

      return response
    except Exception:
      return "NO_CONNECTION"
    
  def cloudsave_creator_deletor(self, request, username):

    headers = {"username": username}
    try:
      response = requests.request("{request}", f'{self.server_url}/api/cloudsaves', headers=headers)
    except Exception:
      return "NO_CONNECTION"

    return response
  
  def delete_cloudsaves(self):

    res = self.cloudsave_creator_deletor("DELETE", self.username)
    if res == "NO_CONNECTION": return "NO_CONNECTION"
    return True
  
  def cloudsave_get(self):

    res = self.cloudsave_creator_deletor("GET", self.username)
    if res == "NO_CONNECTION": return "NO_CONNECTION"
    if res.status_code == 404: return "NOT_EXISTS"
    res = res.text.replace("\"", '')
    return res
  
  def update_cloudsaves(self):
    headers = {
    "username": self.username,
    "data": self.data
    }

    try:
      response = requests.request("PATCH", f'{self.server_url}/api/cloudsaves', headers=headers)
      
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
    try:
      response = requests.request("PUT", f'{self.server_url}/api/cloudsaves', headers=headers)
      return None
    except Exception:
      return "NO_CONNECTION"
    
  def update_cloudsaves(self):
    headers = {
    "username": self.username,
    "data": self.data
    }
    try:
      response = requests.request("PATCH", f'{self.server_url}/api/cloudsaves', headers=headers)
      if response.status_code == 404:
        return "NO_SAVE"
    except Exception:
      return "NO_CONNECTION"

  def get_decryption_key(self):
    key_request = self.query_data("api/server/key")

    decoded_key = key_request.text

    if decoded_key == "NO_CONNECTION":
      return None

    decoded_key = decoded_key.replace("\"", "")
    return decoded_key.encode()
    
  def get_server_name(self):
    try:
      name = requests.request("GET", f'{self.server_url}/api/server/name')
      return name.text
    except Exception:
      return "NO_CONNECTION"
    
  def get_props(self):
    try:
      name = requests.request("GET", f'{self.server_url}/api/properties')
      return name.text
    except Exception:
      return "NO_CONNECTION"
    
  def get_server_version(self):
    try:
      name = requests.request("GET", f'{self.server_url}/api/server/version')
      return name.text
    except Exception:
      return "NO_CONNECTION"
