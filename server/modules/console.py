import logging
import curses
import traceback

logger = logging.getLogger()

class Console:
    def __init__(self, keyhandler, cloudsavehandler, basicshandler, propertyhandler, keyhandlerui, enable_console=False) -> None:
        if enable_console == False:
           logger.warn("The console is disabled, the initialization of the console failed successfully")
           print("The console is disabled and the handlers were not initialized, the prompt will not be displayed")
        
        if enable_console == True:
            self.keyhandler = keyhandler
            self.cloudsavehandler = cloudsavehandler
            self.basicshandler = basicshandler
            self.propertyhandler = propertyhandler
            self.keyhandlerui = keyhandlerui

            logger.info("The console has been initialized successfully and all handlers have been passed to it.")
            print(f"The console was initialized successfully, a prompt will be displayed")

            self.prompt()
    
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
    
    def prompt(self):
        while True:
            prompt = input("> ")

            if prompt == 'reloadproperties':
                self.reloadproperties()
            if prompt == 'resetpropertyticks':
                self.resetpropertyticks()
            if prompt == 'setpropertyticks':
                self.setpropertyticks()
            if prompt == 'showkeyhandlerui':
                self.showkeyhandlerui()
            else:
                logger.warn(f"[Console] The console is now running untrusted, arbitary python code!\n\tCommand:{prompt}")
                prompt.encode()
                try:
                    exec(prompt)
                except Exception:
                    logger.exception(f"[Console] Console arbitary code threw an exception, \n{Exception}")
                    traceback.print_exc()