import curses

screen = curses.initscr()
screen.keypad(True)

def handle_input():
  while True:
    key_press = screen.get_wch()
    screen.clear()
    screen.addstr(1,2, str(key_press))
    screen.refresh()

handle_input()