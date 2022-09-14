class BasicsHandler:
  """
  A class that holds any basic information that has to be passed to the user regularly but doesn't need
  any processing to be done to it before sending, effectively a data class with 1 respond method
  """
  def __init__(self, name, version, key, properties) -> None:
    self.name = name
    self.version = version
    self.key = key
    self.properties = properties

  def respond():
    return "ping"