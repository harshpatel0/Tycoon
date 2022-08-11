import logging
import curses

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class ToggleBox:
  accept_key = 451
  quit_key = 457
  action_key = " "

  screen = None

  def __init__(self, screen) -> None:
    self.screen = screen
    logger.debug(f"Initialized a ToggleBox")
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0) 
    screen.keypad(True)
  
  def handle_inputs(self, toggle_area_positions:tuple, default_value = None):
    try:
      output = not(default_value)
    except Exception:
      output = False
    
    to_return = output

    def update_text_area(text):
      position_y, position_x = toggle_area_positions[0], toggle_area_positions[1]
      self.screen.addstr(position_y, position_x, "       ")
      self.screen.addstr(position_y, position_x, str(text) + " ")
      self.screen.refresh()
      

    while True:
      key_press = self.screen.get_wch()

      if key_press == self.accept_key:
        to_return = output
        break

      if key_press == self.quit_key:
        try:
          to_return = not(default_value)
        except Exception:
          to_return = False
        finally:
          to_return = not(default_value)
        break

      if key_press == self.action_key:
        output = not(output)
        update_text_area(output)
        continue
    logger.debug(f"Choice Box Output: {to_return}")
    return to_return
    
      
  def togglebox(self, title:str, position:tuple, clear_screen:bool = True, button_prompts:bool = True, default_value:bool = None):
    logger.debug(f'Created a togglebox with the following values: Title: {title}, Position: {position}, Clear Screen: {clear_screen}, Button Prompts: {button_prompts}, Default Value: {default_value}')

    position_y, position_x = position[0], position[1]

    self.screen.addstr(position_y, position_x, f"{title}")
    self.screen.addstr(position_y+1, position_x+1, f"Currently set to: ")

    if button_prompts:
      self.screen.addstr(position_y+3, position_x, "Backspace: Num7\tAccept: Num9\tQuit: Num3")

    # Calculate Toggle Area Position

    toggle_area_pos_y = position_y
    toggle_area_pos_x = position_x

    toggle_area_pos_y = toggle_area_pos_y + 1
    toggle_area_pos_x = toggle_area_pos_y + 3
    toggle_area_pos_x = toggle_area_pos_y + len("Currently set to: ")

    toggle_area_pos = (toggle_area_pos_y, toggle_area_pos_x)

    output = self.handle_inputs(toggle_area_positions=toggle_area_pos, default_value=default_value)

    if clear_screen:
      self.screen.clear()
    
    return output