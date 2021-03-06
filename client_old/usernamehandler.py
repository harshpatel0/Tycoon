from generateusername import GenerateUsername
import os

class UsernameHandler():

  def load_uuid_from_file(self):
    with open('username.dat', 'r') as uuidfile:
      self.uuid = uuidfile.read()
      return self.uuid
    
  def save_uuid(self, uuid):

    with open('username.dat', 'w') as uuidfile:
      uuidfile.write(uuid)
      return 0
  
  def check_for_pregenerated_uuid(self):
    if os.path.exists('username.dat'):
      return True
    else:
      return False
    
  def generate_username(self):
    generator = GenerateUsername()    
    generated_uuid = generator.generate_uuid()
    
    self.save_uuid(uuid = generated_uuid)
    
    return generated_uuid
  
  def get_username(self):
    if self.check_for_pregenerated_uuid() == True:
      return self.load_uuid_from_file()
    else:
      return self.generate_username()