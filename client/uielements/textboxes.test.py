import textboxes
import curses

def alphanumerictextbox(screen):
  alphanumerictextbox = textboxes.AlphaNumericTextBox(screen)

  print(alphanumerictextbox.create_textbox("Alpha Numeric TextBox", (1,1), 16))

def numerictextbox(screen):
  numerictextbox = textboxes.NumericTextBox(screen)

  print(numerictextbox.create_textbox("Numeric TextBox", (1,1), 16))

choice = input("1: Alphanumeric, 2: Numeric\n\t")

screen = curses.initscr()

if choice == "1":
  alphanumerictextbox(screen)
else:
  numerictextbox(screen)

curses.endwin()
exit()