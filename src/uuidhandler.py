from cryptography.fernet import Fernet
from advancedgenerateuuid import GenerateUUID

class UUIDHandler():

  uuid = ""

  def check_uuid(self):
    try:
      this_is_a_shit_way_of_doing_things = open('uuid.dat')
      this_is_a_shit_way_of_doing_things.close()

      return 'UUIDEXISTS'
    except IOError:
      return 'UUIDDOESNTEXIST'
    
  def load_uuid(self):
    with open('uuid.dat', 'r') as uuid_file:
      uuid = uuid_file.read()
    
    self.uuid = uuid
    return uuid
    
  def save_uuid(self, uuid):
    with open('uuid.dat', 'w') as uuid_file:
      uuid_file.write(uuid)
    
  def generate_uuid(self):
    generator = GenerateUUID()
    generator.generate_uuid()
    
    generated_uuid = generator.generate_uuid()
    
    self.save_uuid(uuid=generated_uuid)
    self.uuid = generated_uuid

    return generated_uuid