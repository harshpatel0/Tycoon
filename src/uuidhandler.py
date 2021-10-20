import random
from cryptography.fernet import Fernet

FORMAT = "111a1111-a11a-11a1-a111-11111111111"

letters_as_string = 'abcdefghijklmnopqrstuvwxyz'
letters = []

for letter in letters_as_string:
  letters.append(letter)

def generate_letter():
  return random.choice(letters)

def generate_number():
  return random.randint(0, 9)

def check_uuid():
  try:
    this_is_a_shit_way_of_doing_things = open('uuid.dat')
    this_is_a_shit_way_of_doing_things.close()

    return 'UUIDEXISTS'
  except IOError:
    return 'UUIDDOESNTEXIST'
  
def load_uuid():
  with open('uuid.dat', 'r') as uuid_file:
    uuid = uuid_file.read()
  return uuid
  
def save_uuid(uuid):
  with open('uuid.dat', 'w') as uuid_file:
    uuid_file.write(uuid)
  
def generate_uuid():
  final_uuid = ''

  for character in FORMAT:
    if character == '-':
      final_uuid = final_uuid + '-'
    
    elif character.isalpha():
      final_uuid = final_uuid + generate_letter()
    
    else:
      final_uuid = final_uuid + str(generate_number())

  save_uuid(uuid=final_uuid)

  return final_uuid