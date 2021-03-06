from fastapi import FastAPI, Header, Response
from api import API
from keyhandler import Keys

import logging
logging.basicConfig(filename="mainserver.log", format='%(asctime)s %(message)s', filemode="w")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# To edit the property data go to the property_data.py file
from property_data import property_data
# We might need to migrate to Flask instead of FastAPI
# Cuz I can't get this shit to work

# Property data is now stored in the properties class inside the properties file

def keys():
  global key
  keyhandler = Keys()
  if keyhandler.check_key() == False:
    keyhandler.generate_key()
  else:
    keyhandler.load_key()

  key = keyhandler.key

keys()

# Server Properties

app = FastAPI()
api = API()

# Initalize API

api.name = "businessapi"
api.properties = property_data 
api.server_version = 0.01

class Server:
  @app.get("/", status_code = 204)
  def root():
    logger.info("Got a ping request")
    api.respond("ping")

  @app.get("/api/properties")
  def return_props():
    logger.info("Sending property info")
    return api.respond("properties")

  @app.get("/api/server/name")
  def server_name():
    return api.respond("name")

  @app.get("/api/server/server-version")
  def server_version():
    return api.respond("version")

  """"
  This key is decoded to be in string format
  and have to be encoded back to bytes format
  to be used as a key to decrypt
  """
  @app.get("/api/server/key")
  def send_key():
    return key

  # Cloudsave Handler

  @app.get("/api/cloudsaves/")
  def cloudsave_get(response: Response, username = Header(None)):

    if username == None:
      response.status_code = 400
      return None

    cloudsave_response = api.retrieve_cloudsave(username)

    if cloudsave_response == "NOTFOUND":
      response.status_code = 404
      return None
    
    else:
      return cloudsave_response

  @app.put("/api/cloudsaves/", status_code = 201)
  def cloudsave_put(response: Response, username = Header(None), data = Header(None)):

    if data == None or username == None:
      response.status_code = 400

    api.put_cloudsave(username, data)
    return None

  @app.delete("/api/cloudsaves/", status_code = 204)
  def cloudsave_delete(response: Response, username = Header(None)):
    
    if username == None:
      response.status_code = 400
    
    delete_response = api.delete_cloudsave(username)

    if delete_response == "NOTFOUND":
      response.status_code = 404
    
    return None

  # Used to update cloudsaves
  @app.patch("/api/cloudsaves/", status_code = 201)
  def cloudsave_update(response: Response, username = Header(None), data = Header(None)):
    if username == None or data == None:
      response.status_code = 300
    
    patch_response = api.patch_cloudsave(username, data)

    if patch_response == "NOTFOUND":
      response.status_code = 404
    
    return None
