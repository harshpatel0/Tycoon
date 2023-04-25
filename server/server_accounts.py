from flask import Flask, jsonify, request, Response
import modules.keyhandler
import modules.cloudsavehandler
import modules.basicshandler
import modules.accountshandler
import property_data
import logging
import json

logging.basicConfig(filename="server.log", format='%(asctime)s %(message)s', filemode="w")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sessions = {}

app = Flask(__name__)

keyhandler = modules.keyhandler.Keys()
key = keyhandler.get_key()
property_data = property_data.property_data

def load_properties():
  with open('property_data.json', 'r') as propertyfile:
    return json.load(propertyfile)

cloudsavehandler = modules.cloudsavehandler.CloudsaveHandler()
basicshandler = modules.basicshandler.BasicsHandler(name="businessapi", version="0.01", key=key, properties=load_properties())
accountshandler = modules.accountshandler.AccountsHandler(accounts_file_path = 'accounts.json')
# The server is supposed to return a session ID to disallow simultaneous connections, this change should be reflected
# on the client side and the proper calls are to be made

# =============================================================================
"""
Server Information Endpoints
"""

@app.route("/")
def home():
  logger.info("Got a ping request")
  return ""

@app.route("/api/server/name")
def name():
  logger.info(f"Sending server name {basicshandler.name}")
  return basicshandler.name

@app.route("/api/server/version")
def version():
  logger.info(f"Sending server version {basicshandler.version}")
  return basicshandler.version

@app.route("/api/server/key")
def key():
  logger.info(f'Sending server cloudsave decryption key {basicshandler.key}')
  return basicshandler.key

@app.route("/api/properties")
def properties():
  logger.info(f'Sending property data\n\t{basicshandler.properties}')
  return jsonify(basicshandler.properties)

# =============================================================================
"""
Cloudsave Endpoints
"""

@app.route("/api/cloudsaves", methods=['GET'])
def get_cloudsave():
  try:
    username = request.headers['username']
  except KeyError:
    logger.warning('Received a bad request, missing header(s). Discarded request to retrieve save file')
    return Response("Missing username",status=400)

  logger.info(f'Received a cloudsave get request')

  cloudsave_data = cloudsavehandler.get_savefile(username)

  if cloudsave_data == "NOTFOUND":
    logger.warning(f'Couldn\'t find a save file')
    return Response(status=404)
  
  logger.info('Responded with a cloudsave data')
  return cloudsave_data

@app.route("/api/cloudsaves", methods=['PUT'])
def store_cloudsave():
  logger.info('Received a request to store a save data')
  try:
    username, data = request.headers['username'], request.headers['data']
  except Exception:
    logger.warning('Received a bad request, missing header(s). Discarded request to upload save file')
    return Response(status=400)
  cloudsavehandler.save_savefile(data=data, username=username)
  return Response(status=201)

@app.route("/api/cloudsaves", methods=['PATCH'])
def update_cloudsave():
  logger.info('Received a request to store a save data')
  try:
    username, data = request.headers['username'], request.headers['data']
  except KeyError:
    logger.warning('Received a bad request, missing header(s). Discarded request to update save file')
    return Response(status=400)

  output = cloudsavehandler.update_savefile(data=data, username=username)
  if output == "NOTFOUND":
    logger.warn("Save file to update doesn't exist")
    return Response(status=404)
  logger.info('Successfully stored a cloudsave file')
  return Response(status=201)

@app.route('/api/cloudsaves', methods=['DELETE'])
def delete_cloudsave():
  logger.info('Received a request to delete a save data')
  try:
    username = request.headers['username']
  except Exception:
    logger.warning('Received a bad request, missing header(s). Discarded request to delete save file')
    return Response(status=400)

  output = cloudsavehandler.delete_savefile(username=username)
  if output == "NOTFOUND":
    logger.warning("Save file to delete doesn't exist")
    return Response(status=404)
  logger.info('Successfully deleted a cloudsave file')
  return Response(status=200)

# ============================================================================
"""
Account Endpoints
"""
@app.route('/api/accounts', methods=['GET'])
def authorise_login():
    logger.info("Received a request to authorise a login")
    try:
        username, password = request.headers['username'], request.headers['password']
    except KeyError:
        logger.warning("Received a bad request, missing header(s). Discarded Request to Autorise Login")
        return Response(status=400)

    output = accountshandler.authorise_login(username = username, password = password)

    if output == "NOTFOUND":
        return Response(status=404)
    if output == "WRONGPASSWORD":
        # This is a custom HTTP Status Code to indicate that the password is wrong
        return Response(status=435)
    return output

@app.route('/api/accounts', methods=['POST'])
def create_account():
    logger.info("Received a request to create a new account")
    try:
        username, gameusername, password = request.headers['username'], request.headers['gameusername'], request.headers['password']
    except KeyError:
        return Response(status=400)

    output = accountshandler.add_account(username = username, gameusername = gameusername, password = password)
    
    if output == "ALREADYEXISTS":
        return Response(status=436)


if __name__ == "__main__":
  app.run()
