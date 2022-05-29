import curses
import logging
from turtle import pos

class ChoiceBox():
  screen = None
  
  # These don't need to be modified by code, only modified when the core is inherited
  
  backspace_key = 449
  accept_key = 451
  quit_key = 457

  down_arrow = 258
  up_arrow = 259

  text = ""

  def __init__(self, screen, title, position, choices, button_prompts = True, clear_screen = True) -> None:
    self.screen = screen
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0) 
    screen.keypad(True)

    return self.create_choicelist(title, position, choices, button_prompts, clear_screen)

  def create_choicelist(self, title, position, choices, button_prompts, clear_screen):
    if clear_screen:
      self.screen.clear()
    
    position_x = position[0]
    position_y = position[1]

    self.screen.addstr(position_y, position_x, title)

    temp_position_y = position_y
    for choice in choices:
      temp_position_y = temp_position_y + 1
                         #y, x
      self.screen.addstr(temp_position_y, position_x, f"[]{choice}")
    
    if button_prompts:
      temp_position_y + 2
      self.screen.addstr(temp_position_y, position_x, "Backspace: Num7\tAccept: Num9\tQuit: Num3")
    
    temp_position_y = temp_position_y - 2
    return self.handle_inputs(position, choices)
  
  def handle_inputs(self, postion, choices):
    pass
