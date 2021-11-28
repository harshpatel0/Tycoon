import subprocess
import os

class GenerateUUID():

  output_seed = 0

  def get_installed_apps(self):
    
    installed_apps_fullnames = subprocess.check_output([f"{os.getcwd()}\\src\\dependencies\\wmic.exe", "product", "get", "name"]).decode()
    # SHIPPING installed_apps_fullnames = subprocess.check_output([f"{os.getcwd()}\\wmic.exe", "product", "get", "name"])

    installed_apps_fullnames = installed_apps_fullnames.replace('Name', '')
    installed_apps_fullnames = installed_apps_fullnames.replace('\r', '')

    return len(installed_apps_fullnames)
  
  def get_logical_processor_count(self):
    logical_processors = subprocess.check_output(["wmic", "computersystem", "get", "NumberOfLogicalProcessors"]).decode()

    logical_processors = logical_processors.replace('NumberOfLogicalProcessors', '')
    logical_processors = logical_processors.replace('\r', '')

    return int(logical_processors) / 4

  def get_pids(self):
    unprocessed_pids = subprocess.check_output(["wmic", "process", "get", "ProcessID"]).decode()
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

    linebreaks_found = linebreaks_found / 8192

    return round(processed_pids / linebreaks_found)

  def make_seed(self):
    print("Making Seed 1/3")
    self.output_seed = self.get_installed_apps()
    print("Making Seed 2/3")
    self.output_seed = self.output_seed * self.get_logical_processor_count()
    print("Making Seed 3/3")
    self.output_seed = self.output_seed + self.get_pids()

    self.output_seed = int(self.output_seed)

generator = GenerateUUID()
generator.make_seed()
print(generator.output_seed)