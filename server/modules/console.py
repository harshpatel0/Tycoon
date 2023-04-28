import logging
import curses
import traceback

logger = logging.getLogger()

class Console:
    def __init__(self, keyhandler, cloudsavehandler, basicshandler, propertyhandler, keyhandlerui, propertyhandlerui, enable_console=False) -> None:
        if enable_console == False:
           logger.warn("The console is disabled, the initialization of the console failed successfully")
           print("The console is disabled and the handlers were not initialized, the prompt will not be displayed")
        
        if enable_console == True:
            self.keyhandler = keyhandler
            self.cloudsavehandler = cloudsavehandler
            self.basicshandler = basicshandler
            self.propertyhandler = propertyhandler
            self.keyhandlerui = keyhandlerui
            self.propertyhandlerui = propertyhandlerui

            logger.info("The console has been initialized successfully and all handlers have been passed to it.")
            print(f"The console was initialized successfully, a prompt will be displayed")
    
    def reloadproperties(self):
        logger.info("[Console] Force reloaded properties")
        self.propertyhandler.reload_properties()
    
    def resetpropertyticks(self):
        logger.info("[Console] Reset counted ticks")
        self.propertyhandler.ticks = 0
    
    def setpropertyticks(self):
        logger.info("[Console UI] Requesting console new value for counted ticks")
        new_tick = int(input("Tick? "))

        if new_tick == 0:
            logger.info('[Console UI] User backed out of Console UI')
            print("Declined")
            return None
        
        self.propertyhandler.ticks = new_tick
    
    def showkeyhandlerui(self):
        self.keyhandlerui.dashboard()
    
    def showpropertyhandlerui(self):
        self.propertyhandlerui.dashboard()
    
    # def prompt(self):
    #     while True:
    #         logger.debug("Console Prompt Shown")
    #         prompt = input("> ")

    #         if prompt == 'reloadproperties':
    #             self.reloadproperties()
    #             self.prompt()
    #         if prompt == 'resetpropertyticks':
    #             self.resetpropertyticks()
    #             self.prompt()
    #         if prompt == 'setpropertyticks':
    #             self.setpropertyticks()
    #             self.prompt()
    #         if prompt == 'showkeyhandlerui':
    #             self.showkeyhandlerui()
    #             self.prompt()
    #         if prompt == 'showpropertyhandlerui':
    #             self.showpropertyhandlerui()
    #             self.prompt()
    #         if prompt == 'stop' or 'quit':
    #             quit()
    #         else:
    #             logger.warn(f"[Console] The console is now running untrusted, arbitary python code!\n\tCommand:{prompt}")
    #             prompt.encode()
    #             try:
    #                 exec(prompt)
    #                 self.prompt()
    #             except Exception:
    #                 logger.exception(f"[Console] Console arbitary code threw an exception, \n{Exception}")
    #                 traceback.print_exc()
    #                 self.prompt()
    #             except KeyboardInterrupt:
    #                 print("Closed the server")
    #                 quit()

    def prompt(self):
        while True:
            logger.debug("[Console] Reached prompt")
            prompt = input("> ")
            
            logger.warn(f"The console is running the command\n\t\t{prompt}")
            prompt = prompt.encode()
            try:
                exec(prompt)
                continue
            except Exception:
                logger.exception(f'[Console] Prompt threw an exception\n\n{Exception}')
                traceback.print_exc()
                continue