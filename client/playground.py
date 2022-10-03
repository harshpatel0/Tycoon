import curses
from sys import exit
import logging
import json
import modules.datahandlers.backendhandler
import modules.datahandlers.datahandler
import modules.datahandlers.requesthandler
import modules.datahandlers.usernamehandler
import modules.datahandlers.settingshandler
import modules.uielements.textboxes

requesthandler = modules.datahandlers.requesthandler.RequestHandler()
datahandler = modules.datahandlers.datahandler.DataHandler()
usernamehandler = modules.datahandlers.usernamehandler.UsernameHandler()
backendhandler = modules.datahandlers.backendhandler.DataHandler()

screen = curses.initscr()

"""
The playground is used to make user interfaces with proper IntelliSense
"""

class BusinessIdentityManagement:
  def __init__(self, datahandler, requesthandler, screen) -> None:
    self.datahandler = datahandler
    self.requesthandler = requesthandler
    self.screen = screen
    self.main()
  
  def main(self):
    screen.addstr(0,0, "Business Identity Management")
    screen.addstr(1,0, "============================")
    screen.addstr(3,0, f"Name: {datahandler.name}")
    screen.addstr(4,4, "Press [n] to change")
    screen.addstr(6,0, f"Company Name: {datahandler.empire_name}")
    screen.addstr(6,4, "Press [c] to change")
  
  def change_name(self):
    textbox = modules.uielements.textboxes.AlphaNumericTextBox(screen=screen)
    new_name = textbox.create_textbox("What will be the new name for yourself?", position=(0,0), max_chars=12)
    datahandler.change_name(new_name)
    self.main()
  
  def change_empirename(self):
    textbox = modules.uielements.textboxes.AlphaNumericTextBox(screen=screen)
    new_name = textbox.create_textbox("What will be the new name for your company?", position=(0,0), max_chars=10)
    datahandler.change_empire_name(new_name)
    self.main()

def run_playground():
  pass

if __name__ == "__main__":
  run_playground()