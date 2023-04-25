import logging
import random

logger = logging.getLogger()

class BasicsHandler:
  """
  A class that holds any basic information that has to be passed to the user regularly but doesn't need
  any processing to be done to it before sending, effectively a data class with 1 respond method
  """
  def __init__(self, name, version, key) -> None:
    self.name = name
    self.version = version
    self.key = key

  def respond():
    return "ping"


class PropertyHandler:
    """
    A class that handles properties and their reloads
    """
    properties = {}
    
    reload_seconds = 30
    reload_variency = (750, 860, 780, 1990, 810, 2000, 500, 600, 550, 710, 510, 1690)
    reload_variency_factor_probability = ('plus', 'plus', 'minus')

    reload_min_threshold = 600

    # Background
    ticks = 0

    def __init__(self, properties, reload_seconds: int = None, reload_min_threshold: int = None, reload_variency: tuple = None, first_launch_reload: bool = True) -> None:
        self.properties = properties
        
        if reload_variency != None:
            self.reload_seconds = reload_seconds
            self.reload_variency = reload_variency
            self.reload_min_threshold = reload_min_threshold

        logger.info(f"""Initialized PropertyHandler with following
                        Properties: {self.properties}
                        Reload Seconds: {self.reload_seconds}
                        Reload Variency List: {self.reload_variency}
                        Reload Minimum Threshold: {self.reload_min_threshold}""")
        print(f"""Initialized PropertyHandler with following
                        Properties: {self.properties}
                        Reload Seconds: {self.reload_seconds}
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
            print("Reloaded properties!")