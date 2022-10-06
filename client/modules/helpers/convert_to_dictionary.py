import logging
import json

# Intialize Logger
# logging.basicConfig(filename="converttodictionaryhelper.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def convert_to_dictionary(data, name_of_data = "Unspecified"):
  # name_of_data is used for logging
  logger.debug(f"Inital data before converting to dictionary: {data}, Name of data: {name_of_data}")
    
  data = data.replace('\'', '\"')
  logger.debug(f"After double quotting: {data}, Name of data: {name_of_data}")

  data = json.loads(data)
  logger.debug(f"JSON Module Output of Save File: {data}, Name of data: {name_of_data}")

  return data