import logging

logger = logging.getLogger()


class PropertyMarket:
        money, property_count = None, None

        # This will be used to see which property to load and what property the user has chosen to bought
        page = 0

        # Property Data
        properties = {}

        def __init__(self, datahandler, screen) -> None:
            # Desired DataHandlers: DataHandler, screen

            self.datahandler = datahandler
            self.screen = screen

            screen.clear()
            self.init_data()
            # self.render() # Special case
            logger.debug(
                f"Property Market Variables: Money: {self.money} Page: {self.page} Properties: {self.properties}")
            logger.debug(f'Property Data in DataHandler() {datahandler.property_data}')

            self.properties = datahandler.property_data

            self.data_gatherer()
            # self.handle_keypress() # Handled in render funcyion

        def init_data(self):
            self.money = self.datahandler.money
            self.property_count = self.datahandler.property_count

        def data_gatherer(self):
            # First get the keys
            key_list = tuple(self.properties.keys())

            logger.debug(f'Property Keys: {key_list}, Page: {self.page}')
            # Then get the one we want to get
            try:
                data = self.properties[key_list[self.page]]
            except IndexError:
                # Here the page variable has passed higher than what the list actually has
                self.page = len(key_list) - 1
                data = self.properties[key_list[self.page]]

            # Data is assembled here before sending
            page = self.page
            name = key_list[self.page]
            cost = data['cost']
            location = data['location']
            set = data['set']
            description = data['description']
            max_page = len(key_list)
            page = self.page + 1

            logger.debug(
                f'Name: {name}, Cost: {cost}, Location: {location}, Set: {set}, Max Page: {max_page}, Description: {description}')

            details = []

            details.extend([page, name, cost, location, set, description, max_page])
            # self.render(page, max_page, name, cost, location, set, description)

            logger.debug(f'Details in list: {details}')

            self.render(details)

        def handle_buying(self, name):
            # Handle all the outputs of buying properties
            output_of_buy = self.datahandler.handle_all_buy(name)
            self.render_dialog(output_of_buy)
            return None

        def render(self, details):

            name = details[1]
            cost = details[2]
            location = details[3]
            set = details[4]
            description = details[5]
            max_page = details[6]
            page = details[0]

            self.screen.clear()
            # y,x
            self.screen.addstr(0, 0, f"[Q]uit\t\tProperty Market\t\tYou have TY$ {self.money}")
            self.screen.addstr(1, 0, "------------------------------------------------------------------------")
            self.screen.addstr(2, 0, f"Page: {page}/{max_page}")
            self.screen.addstr(4, 0, f"{name}")
            self.screen.addstr(5, 0, f'Price: TY$ {cost}')
            self.screen.addstr(6, 0, f'Located in: {location}\tPart of {set} set')
            self.screen.addstr(8, 0, description)

            # Key help

            def determine_nav_key():
                if page == 1:
                    return "[->]Next Page"
                if page == max_page:
                    return "[<-]Previous Page"
                if page != 1 and page != max_page:
                    return "[<-]Previous Page\t[->]Next Page"

            self.screen.addstr(11, 0, len(f'Located in: {location}\tPart of {set} set') * '-' + (7 * '-'))
            self.screen.addstr(12, 0, f"Buy [SPACE]\t{determine_nav_key()}\t[Q]uit")
            keypress_output = self.handle_keypress()

            if keypress_output == "BUY":
                self.handle_buying(name)

        def handle_keypress(self):
            # Keys
            next_key = 261
            previous_key = 260
            action_key = ' '
            quit_key = 'q'

            key_press = self.screen.get_wch()
            logger.debug(f"Pressed {key_press}")

            if key_press == next_key:
                logger.debug(f"Next Page")
                self.page = self.page + 1
                self.data_gatherer()

            if key_press == previous_key:
                logger.debug(f"Previous Page")
                if self.page != 0:
                    self.page = self.page - 1
                    self.data_gatherer()
                else:
                    self.handle_keypress()

            if key_press == quit_key:
                logger.debug(f"Quit Key")
                return None

            if key_press == action_key:
                logger.debug(f"Buy Key")
                return "BUY"

        def render_dialog(self, message):
            self.screen.clear()
            # y,x
            self.screen.addstr(0, 0, f"[Q]uit\t\tAlert\t\tYou have TY$ {self.money}")
            self.screen.addstr(1, 0, "---------------------------------")
            if message == "SHAMBLES":
                self.screen.addstr(2, 0, "You already own this property")
                self.screen.addstr(3, 0, "And it isn't like you have money to buy it even if you didn't have it")
                self.screen.addstr(4, 0, "Error Code: SHAMBLES")
            if message == "ALREADY PURCHASED":
                self.screen.addstr(2, 0, "You already own this property")
                self.screen.addstr(4, 0, "Error Code: ALREADY PURCHASED")
            if message == "NO FUNDS":
                self.screen.addstr(2, 0, "You don't have enough money to buy this property")
                self.screen.addstr(4, 0, "Error Code: NO FUNDS")
            else:
                self.screen.addstr(2, 0, "The property was successfully bought")
                self.screen.addstr(3, 0, f"You now have $TY {self.datahandler.money}")
            self.screen.addstr(6, 0, "Type any key to go back")

            self.screen.refresh()

            self.screen.get_wch()
            self.screen.clear()
            return None