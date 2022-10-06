print("Loading Core Modules")
import curses
from sys import exit
import logging
print("Initializing DataHandlers")
import modules.datahandlers.backendhandler
import modules.datahandlers.datahandler
import modules.datahandlers.requesthandler
import modules.datahandlers.usernamehandler
import modules.datahandlers.settingshandler
import modules.uielements.textboxes

print("Loading Connections Module")
from modules.helpers.client import connections

# User Interface Imports
print("Loading User Interfaces")
import modules.userinterfaces.businessidentitymanagement
import modules.userinterfaces.propertyportfolio
import modules.userinterfaces.propertymarket

print("Initializing Logger")
logging.basicConfig(filename="main.log", format="%(asctime)s %(message)s", filemode="w")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

client_version = 0.01

print("Setting up Datahandlers")
requesthandler = modules.datahandlers.requesthandler.RequestHandler()
datahandler = modules.datahandlers.datahandler.DataHandler()
usernamehandler = modules.datahandlers.usernamehandler.UsernameHandler()
backendhandler = modules.datahandlers.backendhandler.DataHandler()
# settingshandler = modules.datahandlers.settingshandler.SettingsHandler()

print("Loading screen")
screen = curses.initscr()
print("Done loading")

connector = connections.Connections(
                        requesthandler=requesthandler,
                        datahandler=datahandler,
                        usernamehandler=usernamehandler,
                        backendhandler=backendhandler, screen=screen)

# settings_ui = modules.datahandlers.settingshandler.SettingsUI(screen=screen, raw_settings=settingshandler.raw)

# Server Data 
server_version = None
server_name = None

def quit_app():
    curses.endwin()
    exit()


class Main:
    def __init__(self) -> None:
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        screen.keypad(True)

        connector.connect_to_server()
        connector.retrieve_server_data()

        usernamehandler.get_username()
        logger.debug(f"""
        Datahandlers after successful connections
        DataHandler = {datahandler.save_data}
        BackendHandler = {backendhandler.save_data}
        RequestHandler = {requesthandler.data}
        UsernameHandler = {usernamehandler.username}
        """)
        UserInterface()


class UserInterface:
    def __init__(self) -> None:
        self.Dashboard()

    class Dashboard:
        name, empire_name, money, property_count = None, None, None, None

        def __init__(self) -> None:
            screen.clear()
            self.init_data()
            self.render()
            self.handle_keypress()

        def init_data(self):
            self.name = datahandler.name
            self.empire_name = datahandler.empire_name
            self.money = datahandler.money
            self.property_count = datahandler.property_count

        # Remember the coords are y, x

        def render(self):
            logger.debug(f"Rendering Data in dashboard,\n\tName: {self.name}, Empire Name {self.empire_name}, Money {self.money} Property Count {self.property_count}")
            screen.clear()
            screen.addstr(0, 0, f"{self.empire_name} Dashboard")
            screen.addstr(1, 0, f"Welcome back {self.name}")

            # Render Row Titles
            screen.addstr(4, 0, "Business Statistics")
            screen.addstr(4, 30, "Property Management")

            screen.addstr(5, 0, "-" * 90)

            # Renders the business statistics

            # y, x
            screen.addstr(6, 2, f"Capital: TY$ {self.money}")
            screen.addstr(7, 2, f"Properties: {self.property_count}")

            # Renders property options

            screen.addstr(6, 30, "View [p]roperty Portfolio")
            screen.addstr(7, 30, "Visit the property [m]arket")

            # Renders other options

            # Temporary fix here (Settings Handler)
            if True:
                screen.addstr(9, 0, "[H]elp\t[E]dit Business Documents\t[Q]uit")

            screen.refresh()

        def handle_keypress(self):
            key_press = screen.get_wch()

            if key_press == 'p':
                logger.info("Loading Property Portfolio")
                UserInterface.PropertyPortfolio(datahandler=datahandler, screen=screen)
            if key_press == 'm':
                logger.info("Loading Property Market")
                UserInterface.PropertyMarket(datahander=datahandler, screen=screen)
            if key_press == 'h':
                logger.info("Loading Game Help")
                UserInterface.GameHelp()
            if key_press == 'e':
                logger.info("Loading Business Identity Management")
                UserInterface.BusinessIdentityManagement(datahandler=datahandler, requesthandler=requesthandler, cryptographyhandler=backendhandler.cryptographyhandler, screen=screen)
            if key_press == 's':
                logger.info("Loading Settings Menu")
                logger.warn("The settings menu does not exist")
            if key_press == 'q':
                logger.info("Quitting app")
                logger.debug(f"Cryptography Handler in Dashboard: {backendhandler.cryptographyhandler}")
                datahandler.save(backendhandler.cryptographyhandler)
                exit()
            else:
                self.__init__()

    class PropertyPortfolio:
        def __init__(self, datahandler, screen) -> None:
            self.datahandler = datahandler
            self.screen = screen

            self.load_external_ui()
        
        def load_external_ui(self):
            logger.debug("Loading propertyportfolio External UI")
            modules.userinterfaces.propertyportfolio.PropertyPortfolio(
                datahandler=self.datahandler,
                screen = self.screen
            )

    class PropertyMarket:
        def __init__(self, datahander, screen) -> None:
            self.datahandler = datahander
            self.screen = screen

            self.load_external_ui()
        
        def load_external_ui(self):
            logger.debug("Loading External UI propertymarket")
            modules.userinterfaces.propertymarket.PropertyMarket(
                datahandler=self.datahandler,
                screen=self.screen
            )

    class GameHelp:
        pass

    class BusinessIdentityManagement:
        def __init__(self, datahandler, requesthandler, cryptographyhandler, screen) -> None:
            self.datahandler = datahandler
            self.requesthandler = requesthandler
            self.cryptographyhandler = cryptographyhandler
            self.screen = screen
            self.load_external_ui()
        
        def load_external_ui(self):
            # Business Identity Management requires the datahandler (requiring cryptographyhandler), the requesthandler and the screen
            logger.debug("Loading businessidentitymanagementui External UI")
            modules.userinterfaces.businessidentitymanagement.BusinessIdentityManagement(
                datahandler=self.datahandler, 
                requesthandler=self.requesthandler,
                cryptographyhandler=self.cryptographyhandler,
                screen=self.screen)


def main():
    """This may be used to add additional initialization data"""
    Main()

if __name__ == '__main__':
    main()