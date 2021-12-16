import subprocess
import os
import random

class GenerateSeed():

  seed = 0

  def get_installed_apps(self):
    
    installed_apps_fullnames = subprocess.check_output([f"{os.getcwd()}\\src\\dependencies\\wmic.exe", "product", "get", "name"]).decode()
    # SHIPPING installed_apps_fullnames = subprocess.check_output([f"{os.getcwd()}\\wmic.exe", "product", "get", "name"])

    installed_apps_fullnames = installed_apps_fullnames.replace('Name', '')
    installed_apps_fullnames = installed_apps_fullnames.replace('\r', '')

    return len(installed_apps_fullnames)
  
  def get_logical_processor_count(self):
    logical_processors = subprocess.check_output([f"{os.getcwd()}\\src\\dependencies\\wmic.exe", "computersystem", "get", "NumberOfLogicalProcessors"]).decode()

    logical_processors = logical_processors.replace('NumberOfLogicalProcessors', '')
    logical_processors = logical_processors.replace('\r', '')

    return int(logical_processors) / 4

  def get_pids(self):
    unprocessed_pids = subprocess.check_output([f"{os.getcwd()}\\src\\dependencies\\wmic.exe", "process", "get", "ProcessID"]).decode()
    unprocessed_pids = unprocessed_pids.replace('\r', '')
    unprocessed_pids = unprocessed_pids.replace('ProcessId', '')

    linebreaks_found = 0

    for i in range(len(unprocessed_pids)):
      if(unprocessed_pids[i] == "\n" ):
          linebreaks_found = linebreaks_found + 1
        
    unprocessed_pids = unprocessed_pids.replace('\n', '')
    unprocessed_pids = unprocessed_pids.replace(' ', '')

    processed_pids = 0

    for i in range(len(unprocessed_pids)):
      processed_pids = processed_pids + int(unprocessed_pids[i])

    linebreaks_found = linebreaks_found / 256_000
    return round(processed_pids / linebreaks_found)

  def make_seed(self):
    self.seed = self.get_installed_apps()
    self.seed = self.seed * self.get_logical_processor_count()
    self.seed = self.seed + self.get_pids()

    self.seed = int(self.seed)
  
class GenerateUsername(GenerateSeed):

  FORMATS = ['a1a11aaa1a11aa111a1aaaaaa1a1111aaa11', '1aaa1aaa1a1a1a1aa111a11aa111a1a11a1a', '1aa1111aa11a11111aaa11111a11a11a1111', 'a11a111a-aa11111a11a1a111111111a111a', '111aaaa11111111111a1a11a1aaa11a1a1aa', '11a1aaa1aaaa1a1111a1111a1aaaa1aa1111', '1aaa111111aa11111a11a11111a1aaa1a111', '1a11a11a1a1a111a11aa111a111a1111a111', 'a1a1111aa11a1a1a11a11111aa1111111aaa', 'a11aa1111aa1a11111111111a1a1a11111aa', '11a1a11aa11a1a1aaaa111aa1111111a1aa1', '11111111111aa111aa11aa1111111a1aaa1a', '11111aaaaa11aa1a11a1a11a1a11a1a11111', '111a1a111a1aa11a1a1a11aaa111a1a1111a']
  chosen_format = 0

  NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
  ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

  username = ""

  def pick_format(self):
    random.seed(str(self.make_seed))
    self.chosen_format = random.choice(self.FORMATS)

  def generate_uuid(self):
    random.seed(str(self.make_seed()))
    self.pick_format()
    
    for character in self.chosen_format:
      try:
        int(character)
        self.username = self.username + random.choice(self.NUMBERS)
      except Exception:
        self.username = self.username + random.choice(self.ALPHABET)
        
    return self.username