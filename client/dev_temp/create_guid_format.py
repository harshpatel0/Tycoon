def make_format(guids):
  
  formats = []

  temp_format = ""
  
  for guid in guids:
    for character in guid:
      if character == '-':
        temp_format = temp_format + '-'
      else:
        try:
          int(character)
          temp_format = temp_format + "1"
        except Exception:
          temp_format = temp_format + "a"
    
    formats.append(temp_format)
    temp_format = ""

  return formats

lst = [
  "e7d19afc-d85b-452b-bddb-f7d5665afc39", 
  "8fdb2bcb-b2a8-4ba6-8b25-f858a4a61a8d", 
  "0ff7481d-13e2-477c-b798-3c53a66d8111",
  "a89f852c-ef71-47a0-b8f0-4247127d673e",
  "824adaf6-6581-4677-8f26-1ede11e3f7fb",
  "40b9cfd2-abf0-4238-8334-1eebc3aa2269",
  "4dcb5805-1ac7-418d-9b75-28a5aec1e542",
  "9e14a28e-d2f8-4d69-a589-005b7474d786",
  "d7a1063e-96d3-4f59-8880-be1093045ffa",
  "e95fe846-fe5d-4411-8192-e9c9e11260de",
  "77e6d01f-08e4-4eed-954d-3314449b5ef8",
  "16733605-88db-44af-8bf6-62516b4fdc9f",
  "38346ccd-b35e-4d04-8c00-8e15a1e66252",
  "984b8c29-d9cc-4c1e-a62a-e476b5c8527c"

]

print(make_format(lst))