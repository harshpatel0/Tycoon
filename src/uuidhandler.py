from advancedgenerateuuid import GenerateUUID
import os

class UUIDHandler():

  def load_uuid_from_file(self):
    with open('uuid.dat', 'r') as uuidfile:
      self.uuid = uuidfile.read()
      return self.uuid
    
  def save_uuid(self, uuid):

    with open('uuid.dat', 'w') as uuidfile:
      uuidfile.write(uuid)
      return 0
  
  def check_for_pregenerated_uuid(self):
    if os.path.exists('uuid.dat'):
      return True
    else:
      return False
  
  def generate_uuid(self):
    generator = GenerateUUID()    
    generated_uuid = generator.generate_uuid()
    
    self.save_uuid(uuid = generated_uuid)
    
    return generated_uuid
  
  def get_uuid(self):
    if self.check_for_pregenerated_uuid() == True:
      return self.load_uuid_from_file()
    else:
      return self.generate_uuid()
