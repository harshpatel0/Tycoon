import flask
from flask import request, jsonify
import csv

DEVELOPMENT = True
DEV_ADDR = False

DOWNTIME = False

app = flask.Flask(__name__)

if DEVELOPMENT: 
  app.config["DEBUG"] = True

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

changelog = {
  "Version 1": {
    1: "Increased the prices of 'Friedlander's Office' was 16580 now 36425",
    2: "Decreased the daily profit of 'Friedlander's Office' was 3600 now 1557"
  }
}

version = '0.01'

@app.route('/', methods=['GET'])
def home():
  return '''
  <DOCTYPE html>
  <html>
  <head>
    <title>Business Game Server</title>
  </head>
  
  <body>
    <h1>Business API</h1>
    <p>Unlike WhatsApp, I have a fucking API</p>
    <p><i>Multi-million dollar company can't make their API public</i></p>
    <p>Visit API Links</p>
      <a href="api/properties">Properties</a>
      <a href="api/changelog">Changelog</a>
      <a href="api/version">Version</a>
  </body>
  </html>
  '''

@app.route('/api/check', methods=['GET'])
def validate_server():
  return 'businessapi'

@app.route('/api/server/name', methods=['GET'])
def respond_name():
  return 'Official BusinessAPI'

@app.route('/api/properties', methods=['GET'])
def show_properties():
  return jsonify(properties)

@app.route('/api/changelog', methods=['GET'])
def show_changelog():
  return jsonify(changelog)

@app.route('/api/version', methods=['GET'])
def show_version():
  return version

@app.route('/api/cloudsave/', methods=['GET', 'POST'])
def cloudsave():
  try:
    uuid = request.args["uuid"]
  except Exception:
    return 'BADRESPONSE'

  print(f'{uuid} requested their cloudsave')

  try:
    with open(f'cloudsaves/{uuid}.sav', 'rb') as cloud_save_file:
      cloudsave_data = cloud_save_file.read()

    return cloudsave_data
    
  except FileNotFoundError:
    print("Couldn't find save file on the server")
    return 'NOTFOUND'

if DEV_ADDR:
  app.run()
else:
  app.run(host='0.0.0.0')