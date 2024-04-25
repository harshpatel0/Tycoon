import logging

import eel
from sys import exit

import modules.datahandlers.backendhandler
import modules.datahandlers.datahandler
import modules.datahandlers.requesthandler
import modules.datahandlers.usernamehandler
import modules.datahandlers.settingshandler

eel.init('web')
eel.start('main.html')