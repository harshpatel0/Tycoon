class PropertyPortfolio:

        page = 0
        properties, property_count = None, None
        property_data = None
        money = None

        def __init__(self, datahandler, screen) -> None:
            screen.clear()

            self.screen = screen
            self.datahandler = datahandler

            self.properties = datahandler.properties
            self.property_count = datahandler.property_count
            self.property_data = datahandler.property_data
            self.money = datahandler.money
            logger.debug(f'Properties in save file: {self.properties}')
            self.data_gatherer()

        def render_dialog(self, message):
            screen.clear()
            # y,x
            screen.addstr(0, 0, f"[Q]uit\t\tAlert")
            screen.addstr(1, 0, "---------------------------------")

            if message == "NO PROPERTIES":
                screen.addstr(2, 0, "You don't own any properties")
                screen.addstr(3, 0,
                              "Visit the property market to buy properties, if you think this is an error report the problem")
                screen.addstr(4, 0, "Visit the report a problem guide on the website before reporting a problem")
                screen.addstr(5, 0, "Error Code: NO PROPERTIES")
            if message == "NOT OWNED":
                screen.addstr(2, 0, "You don't own this property")
                screen.addstr(3, 0, "It seems like you don't own this property")
                screen.addstr(4, 0, "This is definately an issue and should be reported")
                screen.addstr(5, 0, "Error Code: NOT OWNED")
            else:
                screen.addstr(2, 0, "Successfully sold")
                screen.addstr(3, 0, f"This property has been sold, you now have TY$ {datahandler.money}")
                self.money = datahandler.money

            screen.addstr(5, 0, "Press ANY KEY to go back to the dashboard")
            screen.refresh()

            screen.get_wch()
            screen.clear()
            return None

        def data_gatherer(self):
            if self.property_count == 0:
                self.render_dialog("NO PROPERTIES")
                UserInterface.Dashboard()

            value_pairs = self.properties

            # Use the value pairs to get the property details from the property data
            try:
                property_info_for_property = self.property_data[value_pairs[self.page]]
            except IndexError:
                self.page = self.page - 1
                property_info_for_property = self.property_data[value_pairs[self.page]]

            logger.debug(
                f'Property Information for the Property {self.page} of owned properties {property_info_for_property}')

            name = value_pairs[self.page]
            location = property_info_for_property['location']
            cost = property_info_for_property['cost']
            set = property_info_for_property['set']
            description = property_info_for_property['description']

            page = self.page + 1
            max_page = self.property_count

            logger.debug(
                f'Name: {name}, Cost: {cost}, Location: {location}, Set: {set}, Max Page: {max_page}, Description: {description}')

            details = []

            details.extend([page, name, cost, location, set, description, max_page, page])

            self.render(details)
            # UserInterface.Dashboard()

        def handle_selling(self, name):
            # Handle all the outputs of buying properties
            output_of_sell = datahandler.handle_all_sell(name)
            self.render_dialog(output_of_sell)
            return None

        def render(self, details):

            name = details[1]
            cost = details[2]
            location = details[3]
            set = details[4]
            description = details[5]
            max_page = details[6]
            page = details[7]

            screen.clear()
            # y,x
            screen.addstr(0, 0, f"[Q]uit\t\tProperty Market\t\tYou have TY$ {self.money}")
            screen.addstr(1, 0, "------------------------------------------------------------------------")
            screen.addstr(2, 0, f"Page: {page}/{max_page}")
            screen.addstr(4, 0, f"{name}")
            screen.addstr(5, 0, f'Price: TY$ {cost}')
            screen.addstr(6, 0, f'Located in: {location}\tPart of {set} set')
            screen.addstr(8, 0, description)

            # Key help

            def determine_nav_key():
                if page == 1:
                    return "[->]Next Page"
                if page == max_page:
                    return "[<-]Previous Page"
                if page != 1 and page != max_page:
                    return "[<-]Previous Page\t[->]Next Page"

            screen.addstr(11, 0, len(f'Located in: {location}\tPart of {set} set') * '-' + (7 * '-'))
            screen.addstr(12, 0, f"Sell [SPACE]\t{determine_nav_key()}\t[Q]uit")

            keypress_output = self.handle_keypress()

            if keypress_output == "SELL":
                self.handle_selling(name)

        def handle_keypress(self):
            # Keys
            next_key = 261
            previous_key = 260
            action_key = ' '
            quit_key = 'q'

            key_press = screen.get_wch()
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
                UserInterface.Dashboard()

            if key_press == action_key:
                logger.debug(f"Sell Key")
                return "SELL"