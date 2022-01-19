import curses

class TextBoxCore():
  screen = None
  
  # These don't need to be modified by code, only modified when the core is inherited
  
  backspace_key = 449
  accept_key = 451

  text = ""

  def __init__(self, screen) -> None:
    self.screen = screen
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)


  def initialize_textbox(self, title, position, max_chars, clear_screen = False, button_prompts = True):
    if clear_screen:
      self.screen.clear()

    # Remove the default parameter for the postion argument

    positon_x = position[0]
    positon_y = position[1]

    self.screen.addstr(positon_y, positon_x, title+":"+"_"*max_chars)
    self.screen.addstr(position[1]+1, positon_x, "Backspace: Num7, Accept: Num9")

    # Finding the TextArea start position

    text_area_pos = len(title)+1

    self.handle_textbox(text_area_pos, position[1], max_chars)

    text = self.text
    self.text = ""
    return text
  
  def finalise(self):
    self.screen.clear()
    return self.text

  def handle_inputs(self, max_chars, position_y, text_area_pos):

    key_press = self.screen.get_wch()
    
    if key_press in self.character_set:
      if len(self.text) == max_chars: return None
      self.text = self.text + key_press
      return None
    
    # Handle Backspace (Keycode 449 or Num7)

    if key_press == self.backspace_key:
      if len(self.text) == 0: return None
      if len(self.text) == 1:
        self.text = ""
        self.screen.addstr(position_y, text_area_pos, "_"*max_chars)
        return None
      self.text = self.text[:-1]

      self.screen.addstr(position_y, text_area_pos, "_"*max_chars)
        
      return None

    if key_press == self.accept_key:
      if len(self.text) == 0: return None
      self.finalise()
      return "DONE"
  
  def display_new_text(self, text_area_pos, position_y):
    self.screen.addstr(position_y, text_area_pos, self.text)
    self.screen.refresh()
  
  def handle_textbox(self, text_area_pos, position_y, max_chars):
    while True:
      opcode = self.handle_inputs(max_chars, position_y, text_area_pos)
      if opcode == "DONE":
        return self.text
      self.display_new_text(text_area_pos, position_y)
    

class AlphaNumericTextBox(TextBoxCore):
  character_set = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

  def __init__(self, screen) -> None:
      super().__init__(screen)

class NumericTextBox(TextBoxCore):

  character_set = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

  def __init__(self, screen) -> None:
    super().__init__(screen)

def run():
  screen = curses.initscr()
  # alphanumerictextbox = AlphaNumericTextBox(screen)
  # print(alphanumerictextbox.initialize_textbox("TextBox", (0,1), 4))

  numerictextbox = NumericTextBox(screen)
  numerictextbox.initialize_textbox("NumericTextBox", (0,1), 4)

if __name__ == "__main__":
  run()