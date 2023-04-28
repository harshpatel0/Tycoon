import random
import logging
import time
import curses
import json

logger = logging.getLogger()

class PropertyHandler:
    """
    A class that handles properties and their reloads
    """
    properties = {}
    
    target_ticks = 30
    reload_variency = (750, 860, 780, 1990, 810, 2000, 500, 600, 550, 710, 510, 1690)
    reload_variency_factor_probability = ('plus', 'plus', 'minus')

    reload_min_threshold = 600

    # Background
    ticks = 0

    def __init__(self, properties, target_ticks: int = None, reload_min_threshold: int = None, reload_variency: tuple = None, first_launch_reload: bool = True) -> None:
        self.properties = properties
        
        if reload_variency != None:
            self.target_ticks = target_ticks
            self.reload_variency = reload_variency
            self.reload_min_threshold = reload_min_threshold

        logger.info(f"""Initialized PropertyHandler with following
                        Properties: {self.properties}
                        Reload Seconds: {self.target_ticks}
                        Reload Variency List: {self.reload_variency}
                        Reload Minimum Threshold: {self.reload_min_threshold}""")

        if first_launch_reload == True:
            self.reload_properties()

    def reload_properties(self):
        keys = tuple(self.properties.keys())
        for key in keys:
            property = dict(self.properties[key])
            base_cost = property['cost']

            variency = random.choice(self.reload_variency)
            variency_modifier = random.choice(self.reload_variency_factor_probability)

            if variency_modifier == 'plus':
                new_cost = base_cost + variency
            else:
                new_cost = base_cost - variency
            
            if new_cost < self.reload_min_threshold:
                new_cost = self.reload_min_threshold
            
            property['cost'] = new_cost
            self.properties[key] = property

            logger.info(f"""Reloaded Property Info
                        Property: {property}
                        Base Cost: {base_cost}
                        Variency Chosen: {variency} {variency_modifier}
                        New Cost: {new_cost}""")
    
    def ticker(self):
        while True:
            logger.debug(f'Running tick, current tick count is on {self.ticks}')
            
            time.sleep(1)
            self.ticks = self.ticks + 1

            if self.ticks == self.target_ticks:
                logging.debug("Tick check for properties has passed, preparing to reload properties")
                self.ticks = 0
                self.reload_properties()
                logging.info('Property costs have been updated')

            continue            


class PropertyDashboard():

    page = 0

    def __init__(self, property_data, textboxes) -> None:
        self.property_data = property_data
        self.textboxes = textboxes

    def render_dashboard(self, screen):
        screen.clear()

        screen.addstr(1,1, "Property Dashboard")
        screen.addstr(3,6, "[V]iew Properties")
        screen.addstr(4,6, "[A]dd new properties")
        screen.addstr(5,6, "[D]elete existing properties")
        screen.addstr(6,6, "[S]ave properties to a properties file")


        screen.addstr(8,6, "E[x]it")
        screen.refresh()

    def render_property(self, details, screen):
        name = details[1]
        cost = details[2]
        location = details[3]
        set = details[4]
        description = details[5]
        max_page = details[6]
        page = details[7]

        screen.clear()
        # y
        screen.addstr(0, 0, f"[Q]uit\t\t[SERVER] Property Portfolio")
        screen.addstr(1, 0, "------------------------------------------------------------------------")
        screen.addstr(2, 0, f"Page: {page}/{max_page}")
        screen.addstr(4, 0, f"{name}")
        screen.addstr(5, 0, f'Price: TY$ {cost}')
        screen.addstr(6, 0, f'Located in: {location}\tPart of {set} set')
        screen.addstr(8, 0, description)

        # Key help

        def determine_nav_key():
            if page == 1:
                return "[>]Next Page"
            if page == max_page:
                return "[<]Previous Page"
            if page != 1 and page != max_page:
                return "[<-]Previous Page\t[->]Next Page"

        screen.addstr(11, 0, len(f'Located in: {location}\tPart of {set} set') * '-' + (7 * '-'))
        screen.addstr(12, 0, f"{determine_nav_key()}\t[Q]uit")

        # This code handles the high level action
        next_key = '.'
        previous_key = ','

        action_key = ' '
        quit_key = 'q'

        key_pressed = screen.get_wch()

        # if keypress == next_key or next_key_2 or dev_next_key:
        #     self.page = self.page + 1
        #     self.gather_property_data(screen)
        
        # elif keypress == previous_key or previous_key_2 or dev_previous_key:
        #     if self.page != 0:
        #         self.page = self.page - 1
        #         self.gather_property_data(screen)
        #     else:
        #         self.render_property(screen=screen, details=details)
        
        # elif keypress == quit_key:
        #     return None
        
        # else:
        #     self.gather_property_data(screen)

        if key_pressed == next_key:
            self.page = self.page + 1
            self.gather_property_data(screen=screen)
        
        elif key_pressed == previous_key:
            if self.page != 0:
                self.page = self.page - 1
                self.gather_property_data(screen=screen)
            else:
                self.render_property(screen=screen, details=details)
        
        elif key_pressed == quit_key:
            return None

        else:
            self.render_property(screen=screen, details=details)

            
    
    def gather_property_data(self, screen):
        # This code is derived off the client from some heavy brainstorming
        # or plain stupidity

        value_pairs = tuple(self.property_data.keys())

        # Use the value pairs to get the property details from the property data
        # try:
        #     property_info_for_property = self.property_data[value_pairs[self.page]]
        # except IndexError:
        #     self.page = self.page - 1
        #     property_info_for_property = self.property_data[value_pairs[self.page]]

        value_pairs = tuple(self.property_data.keys())

        # Use the value pairs to get the property details from the property data
        try:
            property_info_for_property = self.property_data[value_pairs[self.page]]
        except IndexError:
            self.page = self.page - 1
            property_info_for_property = self.property_data[value_pairs[self.page]]


        name = value_pairs[self.page]
        location = property_info_for_property['location']
        cost = property_info_for_property['cost']
        set = property_info_for_property['set']
        description = property_info_for_property['description']

        page = self.page + 1
        max_page = len(self.property_data)

        logger.debug(
                f'Name: {name}, Cost: {cost}, Location: {location}, Set: {set}, Max Page: {max_page}, Description: {description}')

        details = []
        details.extend([page, name, cost, location, set, description, max_page, page])

        self.render_property(details=details, screen=screen)
    
    def delete_property(self, name, screen):
        self.property_data.pop(name)
        
        screen.clear()
        screen.refresh
        screen.addstr(1, 1, "Property Dashboard > Delete Properties")
        screen.addstr(3, 6, f"Deleted {name}")
        screen.addstr(4,6, "Press any key to go back")

        screen.getwch()
        return None

    def save_properties(self, screen):
        with open('property_data.json', 'w') as propertyfile:
            json.dump(self.property_data, propertyfile)
        
        screen.clear()
        screen.refresh()

        screen.addstr(1, 1, "Property Dashboard > Delete Properties")
        screen.addstr(3, 6, f"Saved properties")
        screen.addstr(4,6, "Press any key to go back")

        screen.get_wch()
        return None

    def add_properties(self, screen):
        screen.clear()
        screen.refresh()

        screen.addstr(1, 0, "Property Dashboard > Add Properties")

        textbox = self.textboxes.AlphaNumericTextBox(screen=screen)
        name = textbox.create_textbox("Property Name", (1, 1), 16, clear_screen=True)
        location = textbox.create_textbox("Location", (1, 1), 16, clear_screen=True)
        cost = int(textbox.create_textbox("Cost", (1, 1), 16, clear_screen=True))
        set = textbox.create_textbox("Set", (1, 1), 16, clear_screen=True)
        description = textbox.create_textbox("Description", (1, 1), 32, clear_screen=True)

        property = {
            'name': name,
            'location': location,
            'cost': cost,
            'set': set,
            'description': description
        }
        self.property_data[name] = property

        screen.clear()
        screen.refresh()

        screen.addstr(1, 0, "Property Dashboard > Add Properties")
        screen.addstr(3,6, "Added property successfully")
        screen.addstr(4,6, "Press Any Key to restart")

        screen.get_wch()
        return None

    def dashboard(self):
        if __name__ == '__main__':
            print("This applet is running outside of a server, the files saved may not be in the correct directory and will be ignored by the server.\nYou are recommended to use the console of the server in order to run this applet.\nType 'continue' to continue running the applet")
            if input() == 'continue':
                pass
            else:
                quit()
        
        screen = curses.initscr()
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        curses.curs_set(0)
        
        screen.refresh()

        while True:
            self.render_dashboard(screen)
            screen.refresh()

            event = screen.getch()
            key_pressed = chr(event)

            if key_pressed == 'x':
                break
            if key_pressed == 'v':
                self.gather_property_data(screen=screen)
            if key_pressed == 'a':
                self.add_properties(screen=screen)
            if key_pressed == 'd':
                response = self.gather_property_data(screen=screen)
                self.delete_property(response, screen)
            if key_pressed == 's':
                self.save_properties(screen=screen)
        
        if __name__ == "__main__":
            quit()
        else:
            curses.endwin()
            return None
