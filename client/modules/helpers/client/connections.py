import modules.uielements.textboxes
import logging

logger = logging.getLogger()


class Connections:
    def __init__(self, requesthandler, backendhandler, datahandler, usernamehandler, screen,
                 debug_skip_ip: bool = False, debug_use_ip: str = "127.0.0.1",
                 debug_skip_new_save_file_message: bool = False,
                 debug_skip_name_when_creating_new_save_files: bool = False,
                 debug_create_save_file_with_name: bool = "TestName",
                 debug_skip_empire_name_when_creating_new_save_files: bool = False,
                 debug_create_save_file_with_empire_name: bool = "TestEmpire"):

        self.requesthandler = requesthandler
        self.backendhandler = backendhandler
        self.datahandler = datahandler
        self.usernamehandler = usernamehandler

        self.screen = screen

        self.debug_skip_ip = debug_skip_ip
        self.debug_use_ip = debug_use_ip
        self.debug_skip_new_save_file_message = debug_skip_new_save_file_message
        self.debug_skip_name_when_creating_new_save_files = debug_skip_name_when_creating_new_save_files
        self.debug_create_save_file_with_name = debug_create_save_file_with_name
        self.debug_skip_empire_name_when_creating_new_save_files = debug_skip_empire_name_when_creating_new_save_files
        self.debug_create_save_file_with_empire_name = debug_create_save_file_with_empire_name

    def create_new_save_file_wizard(self):
        if not self.debug_skip_new_save_file_message:
            self.screen.clear()
            self.screen.addstr(0, 0, "Create a new save file")
            self.screen.addstr(1, 0, "----------------------")
            self.screen.addstr(2, 0, "You don't have a save file on this server so we will need to create")
            self.screen.addstr(3, 0, "a new one, you will be asked to input the name of your character")
            self.screen.addstr(4, 0, "and what you want to call your company, press any key to continue")
            self.screen.refresh()

            self.screen.get_wch()

        self.screen.clear()
        textbox = modules.uielements.textboxes.AlphaNumericTextBox(screen=self.screen)
        if not self.debug_skip_name_when_creating_new_save_files:
            name = textbox.create_textbox("Your Name", (1, 1), 16)
        else:
            name = self.debug_create_save_file_with_name
        if not self.debug_skip_empire_name_when_creating_new_save_files:
            empire_name = textbox.create_textbox("Your Empire Name", (1, 1), 16)
        else:
            empire_name = self.debug_create_save_file_with_empire_name

        if name == "QUIT" or empire_name == "QUIT":
            self.screen.clear()
            self.screen.addstr(0, 0, "Error")
            self.screen.addstr(1, 0, "-----")
            self.screen.addstr(2, 0, "You cannot have a blank name or empire name, do you want to try again?")
            self.screen.addstr(3, 0, "Press any key to retry or press q to quit app")

            keypress = self.screen.get_wch()

            if keypress == "q":
                exit()

            self.create_new_save_file_wizard()

        self.screen.clear()
        self.backendhandler.generate_save_file(name=name, empire_name=empire_name)
        return self.backendhandler.save_data

    def connect_to_server(self):
        if not self.debug_skip_ip:
            ipaddress_textbox = modules.uielements.textboxes.AddressTextBox(screen=self.screen)

            ipaddress = ipaddress_textbox.create_textbox("Server Address", (1, 1), 19)

            self.screen.refresh()
            if ipaddress == "QUIT":
                quit()
        else:
            ipaddress = self.debug_use_ip

        self.screen.clear()
        self.screen.addstr(1, 2, f"Connecting to {ipaddress}")
        self.screen.refresh()

        self.requesthandler.server_url = f"http://{ipaddress}"
        status = self.requesthandler.ping()

        if status != "NO_CONNECTION":
            self.screen.clear()

        else:
            self.screen.clear()

            self.screen.addstr(1, 2, f"Couldn't connect to {ipaddress}")
            self.screen.addstr(2, 4, "A connection to a server is needed to play")
            self.screen.addstr(3, 4, "[R]etry, Any other key to exit")

            self.screen.refresh()

            keypress = self.screen.get_wch()

            if keypress == "r":
                self.screen.clear()
                self.requesthandler.server_url = None
                self.connect_to_server()
            else:
                quit()

    def retrieve_server_data(self):
        self.screen.clear()

        self.screen.addstr(0, 0, "Loading")
        self.screen.addstr(1, 0, "-------")
        self.screen.refresh()

        self.screen.addstr(3, 1, "Generating Username")
        self.screen.addstr(4, 1, "[-     ]")
        self.screen.refresh()

        self.requesthandler.username = self.usernamehandler.get_username()
        logger.debug(f'Username: {self.requesthandler.username}')

        self.screen.addstr(3, 1, "Initializing Datahandlers (1/2)\t\t\t\t\t\t")
        self.screen.addstr(4, 1, "[--    ]")
        self.screen.refresh()

        self.backendhandler.fill_arguments(server_url=self.requesthandler.server_url,
                                           username=self.requesthandler.username)

        self.backendhandler.fill_decryption_key_field()

        logger.debug(
            f'Backend Handler Filled Arguments: Server URL: {self.requesthandler.server_url}'
            f'Username: {self.requesthandler.username}\nDecryption Key: {self.backendhandler.key}, '
            f'Cryptography Handler: {self.backendhandler.cryptographyhandler}')

        self.datahandler.cryptographyhander = self.backendhandler.cryptographyhandler
        logger.debug("Passed cryptography handler to DataHandler")

        self.screen.addstr(3, 1, "Initializing Datahandlers (2/2)\t\t\t")
        self.screen.addstr(4, 1, "[---   ]")
        self.screen.refresh()
        self.datahandler.fill_property_data()
        logger.debug(f'Loading Stage 3: Called fill property data, property data={self.datahandler.property_data}')

        self.screen.addstr(3, 1, "Loading Save File\t\t\t\t")
        self.screen.addstr(4, 1, "[----  ]")
        self.screen.refresh()
        logger.debug(f'Loading Stage 4: Parsing Save file')
        save_data = self.backendhandler.get_save_file()

        if save_data == "GENERATE":
            logger.warning("User doesn't have a save file on this server, creating new one")
            self.datahandler.save_data = self.create_new_save_file_wizard()
        else:
            self.datahandler.save_data = save_data

        self.datahandler.save_file_parser()

        self.screen.addstr(3, 1, "Gathering Information (1/2)\t\t\t")
        self.screen.addstr(4, 1, "[----- ]")
        self.screen.refresh()
        server_name = self.requesthandler.get_server_name()

        self.screen.addstr(3, 1, "Gathering Information (2/2)")
        self.screen.addstr(4, 1, "[------]")
        self.screen.refresh()
        server_version = self.requesthandler.get_server_version()

        # encrypted_save = self.requesthandler.cloudsave_get()
        # encrypted_save = encrypted_save.encode()

        # Handled by datahandler.get_save_file() function

        logger.info(f"Connected to {server_name} on version {server_version}"
                    f" on IP Address {self.requesthandler.server_url}")

        self.backendhandler.get_property_data()

        logger.debug(f"Property Data: {self.backendhandler.property_data}")
        self.screen.addstr(3, 1, "Loading Game")
        self.screen.refresh()

        logger.debug("Loading User Interface")
        return None
