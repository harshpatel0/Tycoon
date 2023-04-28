import modules.propertyhandler
import modules.textboxes
import json

def load_properties():
  with open('test_property_data.json', 'r') as propertyfile:
    return json.load(propertyfile)

propertyhandlerui = modules.propertyhandler.PropertyDashboard(property_data=load_properties(), textboxes=modules.textboxes)

propertyhandlerui.dashboard()