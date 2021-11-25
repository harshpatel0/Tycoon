from fastapi import FastAPI, Header, Response
import json

properties = {
  "Amy's Baking Company": {
    'dailyExpenses': 750,
    'dailyProfit': 189,
    'cost': 8380,
    'location': "Somewhere idk",
    'set': "Gordon Ramsay"
  },

  "Friedlander's Office": {
    'dailyExpenses': 153,
    'dailyProfit': 1557,
    'cost': 36425,
    'location': "Los Santos Highway",
    'set': "Grand Theft Auto Property Pack"
  },

  "Roman's Cabs": {
    'dailyExpenses': 254,
    'dailyProfit': 472,
    'cost': 7586,
    'location': 'Bohan',
    'set': "Grand Theft Auto Property Pack"
  },

  'Anteiku': {
    'dailyExpenses': 124,
    'dailyProfit': 345,
    'cost': 10571,
    'location': "Tokyo, Japan",
    'set': "Tokyo Ghoul"
  },

  'Test Joint': {
    'dailyExpenses': 9999,
    'dailyProfit': 99999,
    'cost': 999999,
    'location': 'Your motha',
    'set': 'Buy this i fucking dare u'
  },
}

# Server Properties

class API():
  name = ""
  properties = {}
  version = 0

  def respond(self, query):

    if self.name == "" or self.properties == {} or self.version == 0:
      return "API not initialized"
    if query == "ping":
      return 1
    if query == "properties":
      return self.properties
    if query == "name":
      return self.name
    if query == "version":
      return self.version
  
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
    
app = FastAPI()

api = API()

# Initalize API

api.name = "businessapi"
api.properties = properties
api.version = 0.01

@app.get("/", status_code = 204)
def root():
  api.respond("ping")

@app.get("/api/properties")
def root():
  return api.respond("properties")

@app.get("/api/server/name")
def root():
  return api.respond("name")

@app.get("/api/server/version")
def root():
  return api.respond("version",)

@app.get("/api/cloudsaves/{uuid}")
def cloudsave_get(uuid, response: Response ):
  cloudsave_response = api.retrieve_cloudsave(uuid)

  if cloudsave_response == "NOTFOUND":
    response.status_code = 404
  
  else:
    return cloudsave_response

@app.put("/api/cloudsaves/{uuid}", status_code = 201)
def cloudsave_put(uuid, data = Header(None)):
  if data == None:
    return "BAD"
  api.put_cloudsave(uuid, data)