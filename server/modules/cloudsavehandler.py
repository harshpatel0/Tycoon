import os

class CloudsaveHandler():
  """
  This handles the cloudsaves
  """
  cloudsave_path = "cloudsaves/"
  
  def get_savefile(self, username):
    try:
      with open(f'{self.cloudsave_path}/{username}.sav', 'rb') as savefile:
        return savefile.read()
    except FileNotFoundError:
      return 'NOTFOUND'
    
  def save_savefile(self, data, username):
    data = data.encode('utf-8')
    with open(f'{self.cloudsave_path}/{username}.sav', 'wb') as savefile:
      savefile.write(data)
    
  def delete_savefile(self, username):
    try:
      os.remove(f'{os.getcwd()}/{self.cloudsave_path}/{username}.sav')
    except Exception:
      return 'NOTFOUND'
    
  def update_savefile(self, data, username):
    data = data.encode('utf-8')
    method_output = self.delete_savefile()
    if method_output == "NOTFOUND":
      return "NOTFOUND"
    with open(f'{self.cloudsave_path}/{username}.sav', 'wb') as savefile:
      savefile.write(data)