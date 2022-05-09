# Plans

## Urgent
- Improve the User Interface
  - Change the dashboard to a menu style instead of pressing seemingly random keys
- Improve the Keybinds
- Code out the settings functionality
  - Settings menu to change settings
  - Change controls
- Compile the code
- Add a property data management function to easily add and remove properties

## Less Urgent
- Add the option to enable auto-reload which will allow the client to reload property data so that
property data could be changed on the fly and the clients would reload it
- Add an option for the settings to pass certain rules or settings and have the client respond to them
  - `enable-hot-reload-for-properties`
  - `generate-usernames-on-server`

  API Endpoint = `http://{server_url}/api/server/settings` -> List

- Generate usernames on the server instead of the client

  API Endpoint = `http://{server_url}/api/cloudsaves/generate_username/` -> String

## Low Priority (For Now)
- Either make a client using Python Eel or a UI Library like Tkinter or PyQt5