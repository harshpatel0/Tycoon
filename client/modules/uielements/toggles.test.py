import curses 
import toggles
import logging

logging.basicConfig(filename="toggles.log", format="%(asctime)s %(message)s", filemode="w")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

screen = curses.initscr()

togglebox = toggles.ToggleBox(screen=screen)
output = togglebox.togglebox("Debug Togglebox", position=(0,0), clear_screen=True, button_prompts=True, default_value=None)

screen.clear()

screen.addstr(0,0, str(output) + ", press any key to quit")

screen.get_wch()