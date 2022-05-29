# Property Data format
# id - Now used as the name for the properties
  # name - Depricated, you wouldn"t want to have 2 properties with the same name anyway
  # cost
  # location
  # set

# To add a property

# First copy the first part of the code until where it says "Property data for this property ends here"
# Then paste it again below the one you copied from
# Then make sure you change the first part before the colon as this is the property name and must be unique

# NB: Make sure not to remove the single quotes and the property name can"t be the same

property_data = {
  'Oscars Kinyozi': {
    'cost': 8800,
    'location': 'South C',
    'set': 'Starter',
    'description': 'Dont cheat on this barber and get\nthe best fade the world has ever seen'
  },

  # Property Data for this property ends here

  'Appul': {
    'cost': 2000,
    'location': 'Definately the USA',
    'set': 'Chinese Copy',
    'description': 'Just like real apple son, it has\nA unlike your report card'
  },
}