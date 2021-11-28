import requests
import curses
from cryptography.fernet import Fernet
from propertydataloader import download_property_data, load_local_property_data
from checkversion import check_version
from time import sleep
import savedata
from uuidhandler import UUIDHandler
import inquirer

VERSION = 0.01
connected_to_servers = False

uuid_handler = UUIDHandler()
uuid = uuid_handler.get_uuid()

ENCRYPTOR = Fernet(b'jm3YewpnyOAnk-tyXNsN9mx0ZLYtnaASuKsaPoYNxhk=')

def connect_to_servers(address):
  if address == '':
    return 'FAILED'

  print(f'Connecting to {address}')
  try:
    r = requests.get(f'http://{address}:5000/api/check')
  except requests.exceptions.ConnectionError:
    return 'FAILED'

  if r.text == 'businessapi':
    sleep(2)
    return 'SUCCESS'
  elif r.text == 'DOWN':
    return 'DOWN'
  else:
    return 'FAILED'

connectivity_prompt = [
  inquirer.List("connectivity-prompt",
                message="Do you want to connect to a game server",
                choices=["Yes", "No"])
]

server_address = [
  inquirer.Text('server_address', 
  message="Type the server address")
]

connectivity_prompt = inquirer.prompt(connectivity_prompt)
connectivity_prompt = sorted(set(connectivity_prompt.values()), reverse=True)[-1]

if connectivity_prompt == 'Yes':
  server_address = inquirer.prompt(server_address)
  server_address = sorted(set(server_address.values()), reverse=True)[-1]
  status = connect_to_servers(server_address)

  if status == 'SUCCESS':
    connected_to_servers = True
    print("Successfully connected to the API")

  elif status == 'DOWN':
    print("This server is currently down, switching to offline mode")

  else:
    print("Unable to connect/verify server, switching to offline mode")
  
else:
  pass

if connected_to_servers:
  version_check_status = check_version(server_address, VERSION)
  sleep(2)

  if version_check_status == 'UPTODATE':
    print("You are running the latest version")
  elif version_check_status == 'NEEDSUPDATE':
    print(f"There is an update for this game, download the update by\ntyping https://{server_address}:5000/downloads in your web browser")
    print("Press ENTER to skip the current update")
    input()
    print("Skipped update, you might not be able to purchase newer properties")
  elif version_check_status == 'WTF':
    print("Your game reports that it is newer than the current server version, please redownload your game")

  property_data = download_property_data(server_address)
  sleep(2)

else:
  property_data = load_local_property_data()

# Getting the game save data

game_save_existance_status = savedata.check_save()

if game_save_existance_status == 'SAVEEXISTS':
  savedata.load_save()

else:
  if connected_to_servers:
    
    request_cloud_save_prompt = [
      inquirer.List(
      'request_cloud_save_prompt', 
      message="Would you like to download your game data from the server", 
      choices=['Yes', 'No'],
      ),
    ]
    
    request_cloud_save_prompt = inquirer.prompt(request_cloud_save_prompt)
    request_cloud_save_prompt = sorted(set(request_cloud_save_prompt.values()), reverse=True)[-1]

    if request_cloud_save_prompt.lower() == 'yes':
      clouddata_response = savedata.cloudsave(address=server_address, uuid=uuid)

      if clouddata_response == 'FAILED':
        print("Failed to retrieve cloud data")
        print("Creating a save file")
        game_data = savedata.create_save()

      elif clouddata_response == 'NOTFOUND':
        print("Your cloudsave data wasn't found")
        print("Creating a save file")
        game_data = savedata.create_save()
      
      else:
        game_data = clouddata_response
    
    else:
      game_data = savedata.create_save()

class Game():
  def __init__(self) -> None:
    self.dashboard()
      
  def settings(self, screen, game_data):
    while True:
      self.render_text_objects(screen, game_data, "Settings")
      screen.refresh()

      event = screen.getch()
      key_pressed = chr(event)

      if key_pressed == 'p':
        self.change_profile_name()
      if key_pressed == 'e':
        self.change_empire_name()
      if key_pressed == 'b':
        return None

  def render_text_objects(self, screen, game_data, to_render):
    # Parse Save file
    screen.clear()

    profile_name = game_data['profileName']
    empire_name = game_data['empireName']
    capital = game_data['capital']
    owned_businesses = game_data['ownedBusinesses']
    businesses = game_data['businesses']

    screen.clear()

    max_rows, max_cols = screen.getmaxyx()
    mid_row = int(max_rows / 2)
    mid_col = int(max_cols / 2)

    if to_render == "dashboard":
      # Remember its y,x.
      # IDK what the curses devs were drinking that day
      # They say its because it was like that when it came out but come on now
      # get a hold of yourselves @CursesDevs

      length_of_capital = 0
      for number in str(capital):
        length_of_capital = length_of_capital + 1

      screen.addstr(1,1, f"{empire_name} Dashboard")
      screen.addstr(1, max_cols-10, "Settings")
      screen.addstr(2, max_cols-10, "Logout")

      screen.addstr(6, 6, str(capital))
      screen.addstr(7, 6, "Capital")

      screen.addstr(6, 25, "View properties")
      screen.addstr(7, 25, "Purchase more properties")
      
      if connected_to_servers:
        screen.addstr(2,1, f"Connected to corprate network")
      else:
        screen.addstr(2,1, f"Couldn't connect to corprate network")
      
      return None

    if to_render == 'settings':
      screen.addstr(1,1, "Settings")
      screen.addstr(4,1, f"Profile Name: {profile_name}")
      screen.addstr(4, 40, "Type p to change profile name")
      screen.addstr(5,1, f"Empire Name: {empire_name}")
      screen.addstr(5, 40, "Type e to change empire name")
      
      if connected_to_servers:
        screen.addstr(8, 1, f"Connected to {server_address}")
      else:
        screen.addstr(8,1, "Not connected to servers")

  def dashboard(self):
    running = True
    screen = curses.initscr()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.curs_set(0)

    while running:
      self.render_text_objects(screen, game_data, "dashboard")
      screen.refresh()

      event = screen.getch()
      key_pressed = chr(event)

      if key_pressed == 'v':
        self.view_properties()
      if key_pressed == 'l':
        break
      if key_pressed == 's':
        self.settings()
    
    curses.endwin()
    
Game()