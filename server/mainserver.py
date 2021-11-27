from fastapi import FastAPI, Header, Response
from api import API

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
def return_props():
  return api.respond("properties")

@app.get("/api/server/name")
def server_name():
  return api.respond("name")

@app.get("/api/server/version")
def server_version():
  return api.respond("version")

# Cloudsave Handler

@app.get("/api/cloudsaves/")
def cloudsave_get(response: Response, uuid = Header(None)):

  if uuid == None:
    response.status_code = 400
    return None

  cloudsave_response = api.retrieve_cloudsave(uuid)

  if cloudsave_response == "NOTFOUND":
    response.status_code = 404
    return None
  
  else:
    return cloudsave_response

@app.put("/api/cloudsaves/", status_code = 201)
def cloudsave_put(response: Response, uuid = Header(None), data = Header(None)):

  if data == None or uuid == None:
    response.status_code = 400

  api.put_cloudsave(uuid, data)
  return None

@app.delete("/api/cloudsaves/", status_code = 204)
def cloudsave_delete(response: Response, uuid = Header(None)):
  
  if uuid == None:
    response.status_code = 400
  
  delete_response = api.delete_cloudsave(uuid)

  if delete_response == "NOTFOUND":
    response.status_code = 404
  
  return None


# Used to update cloudsaves
@app.patch("/api/cloudsaves/", status_code = 201)
def cloudsave_update(response: Response, uuid = Header(None), data = Header(None)):
  if uuid == None or data == None:
    response.status_code = 300
  
  patch_response = api.patch_cloudsave(uuid, data)

  if patch_response == "NOTFOUND":
    response.status_code = 404
  
  return None
