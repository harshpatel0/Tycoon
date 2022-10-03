from modules.uielements import textboxes

class BusinessIdentityManagement:
  def __init__(self, datahandler, requesthandler, screen) -> None:
    screen.clear()
    self.datahandler = datahandler
    self.requesthandler = requesthandler
    self.screen = screen
    self.main()
  
  def main(self):
    self.screen.addstr(0,0, "Business Identity Management")
    self.screen.addstr(1,0, "============================")
    self.screen.addstr(3,0, f"Name: {self.datahandler.name}")
    self.screen.addstr(4,4, "Press [n] to change")
    self.screen.addstr(6,0, f"Company Name: {self.datahandler.empire_name}")
    self.screen.addstr(6,4, "Press [c] to change")
  
  def change_name(self):
    textbox = textboxes.AlphaNumericTextBox(screen=self.screen)
    new_name = textbox.create_textbox("What will be the new name for yourself?", position=(0,0), max_chars=12)
    self.datahandler.change_name(new_name)
    self.main()
  
  def change_empirename(self):
    textbox = textboxes.AlphaNumericTextBox(screen=self.screen)
    new_name = textbox.create_textbox("What will be the new name for your company?", position=(0,0), max_chars=10)
    self.datahandler.change_empire_name(new_name)
    self.main()