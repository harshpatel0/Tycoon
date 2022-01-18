class InventoryHandler:
  save_data = None

  def initialize(self, save_file):
    self.save_data = save_file
    return 1
  
  def save_parser(self, query):
    return self.save_data[query]
  
  def save(self, query, data):
    self.save_data[query] = data
    return None

  def remove_money(self, amount):
    money = self.save_parser("money")
    money = money - amount

    self.save("money", money)
  
  def add_money(self, amount):
    money = self.save_parser("money")
    money = money + amount

    self.save("money", money)
  
  def add_property(self, property_name):
    properties = list(self.save_parser("properties"))
    properties.append("property_name")
    self.save("properties", properties)
