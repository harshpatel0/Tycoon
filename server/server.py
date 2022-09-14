import flask
import modules.keyhandler
import modules.cloudsavehandler
import modules.basicshandler
import property_data

keyhandler = modules.keyhandler.Keys()
key = keyhandler.get_key()
property_data = property_data.property_data

cloudsavehandler = modules.cloudsavehandler.CloudsaveHandler()
basicshandler = modules.basicshandler.BasicsHandler(name="businessapi", version="0.01", key=key, properties=property_data)


