import requests

def check_version(address, client_version):
  print("Checking for a new version")

  r = requests.get(f'http://{address}:5000/api/version')
  server_version = float(r.text)

  if server_version == client_version:
    return 'UPTODATE'
  if server_version > client_version:
    return 'NEEDUPDATE'
  if server_version < client_version:
    return 'WTF'