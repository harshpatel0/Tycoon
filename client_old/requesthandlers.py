import requests

class RequestHandler():
  server_address = ""

  def get_key(self):
    return requests.request("GET", f"http://{self.server_address}:8000/api/server/key").text
  
  def get_version(self):
    return requests.request("GET", f"http://{self.server_address}:8000/api/server/version").text

  def get_name(self):
    return requests.request("GET", f"http://{self.server_address}:8000/api/server/name").text

  def get_properties(self):
    return requests.request("GET", f"http://{self.server_address}:8000/api/properties").text

  def get_cloudsaves(self, username):
    headers = {"username": f"{username}"}
    response = requests.request("GET", f"http://{self.server_address}:8000/api/cloudsaves/", headers=headers)
  
  def upload_cloudsaves(self, username, encrypted_save_file):
    headers = {
        "data": encrypted_save_file,
        "uuid": f"{self.username}"
    }

    requests.request("PUT", f"http://{self.server_address}:8000/api/cloudsaves/", headers=headers)
    return None