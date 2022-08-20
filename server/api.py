import os

class API:

  name = ""
  properties = {}
  server_version = 0

  def respond(self, query):

    """Responds with data about the server

    Returns:
        [String]: [data]
    """

    if self.name == "" or self.properties == {} or self.server_version == 0:
      return "API not initialized"
    if query == "ping":
      return 1
    if query == "properties":
      return self.properties
    if query == "name":
      return self.name
    if query == "version":
      return self.server_version
  
  def retrieve_cloudsave(self, uuid):

    try:
      with open(f'cloudsaves/{uuid}.sav', 'rb') as cloud_save_file:
        cloudsave_data = cloud_save_file.read()

      return cloudsave_data
      
    except FileNotFoundError:
      return 'NOTFOUND'
    
  
  def put_cloudsave(self, uuid, data):
    data = data.encode('utf-8')
    with open(f'cloudsaves/{uuid}.sav', 'wb') as cloud_save_file:
      cloud_save_file.write(data)
    
  def delete_cloudsave(self, uuid):
    try:
      os.remove(f'{os.getcwd()}/cloudsaves/{uuid}.sav')
      return 1
    except Exception:
      return "NOTFOUND"
    
  def patch_cloudsave(self, uuid, data):

    data = data.encode('utf-8')
    try:
      save_file = open(f"cloudsaves/{uuid}.sav", 'rb')
      save_file.close()

    except Exception:
      return "NOTFOUND"

    os.remove(f"{os.getcwd()}/cloudsaves/{uuid}.sav")
    with open(f'cloudsaves/{uuid}.sav', 'wb') as file:
      file.write(data)
    
    return None