characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
list = []

for character in characters:
  try:
    list.append(str(character))
  except:
    list.append(character)
print(list)