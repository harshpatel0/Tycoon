from modules.uielements import textboxes

class BusinessIdentityManagement:
  def __init__(self, datahandler, requesthandler, cryptographyhandler, screen) -> None:
    screen.clear()
    self.datahandler = datahandler
    self.requesthandler = requesthandler
    self.screen = screen
    self.cryptographyhandler = cryptographyhandler
    self.render()
  
  def render(self):
                      #y,x
    self.screen.addstr(0,0, "Business Identity Management")
    self.screen.addstr(1,0, "=======================================")
    self.screen.addstr(3,0, f"Name: {self.datahandler.name}")
    self.screen.addstr(4,2, "Press [n] to change")
    self.screen.addstr(6,0, f"Company Name: {self.datahandler.empire_name}")
    self.screen.addstr(7,2, "Press [c] to change")
    self.screen.addstr(9,0, "[S]ave Changes and Exit")

    self.handle_keypress()
    return None
  
  def handle_keypress(self):
    keypress = self.screen.get_wch()

    if keypress == 'b':
      return None
    if keypress == 'n':
      self.change_name()
    if keypress == 'c':
      self.change_empirename()
  
  def change_name(self):
    textbox = textboxes.AlphaNumericTextBox(screen=self.screen)
    new_name = textbox.create_textbox("What will be the new name for yourself?", position=(0,1), max_chars=20)
    self.datahandler.name = new_name
    self.datahandler.save(self.cryptographyhandler)
    self.render()
  
  def change_empirename(self):
    textbox = textboxes.AlphaNumericTextBox(screen=self.screen)
    new_name = textbox.create_textbox("What will be the new name for your company?", position=(0,1), max_chars=32)
    self.datahandler.empire_name = new_name
    self.datahandler.save(self.cryptographyhandler)
    self.render()