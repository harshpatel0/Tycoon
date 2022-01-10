import curses


connected_to_servers = True

server_address = '192.168.0.106'

game_data = {
    "profileName": 'Test Joint',
    "empireName": 'Test Joint Inc',
    "capital": 9_999_999,
    "ownedBusinesses": 0,
    "businesses": []
  }

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