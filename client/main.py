from os import system
import curses
import requesthandler
import datahandler
import usernamehandler
import inventoryhandler

import uielements.textboxes


class Main():
  
  screen = curses.initscr()

  