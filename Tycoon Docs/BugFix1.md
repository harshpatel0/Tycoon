# Bug Fix 1

## All
- Fixed imports so modules would be imported
- Fixed all errors so the game can actually load

## Client Main
- Fixed a bug where the screen won't be cleaned when failing to connect to the server
- Added a quit option to the address text box
- When Loading the game after connecting, the loading has been made more verbose

## Request Handler
- Fixed an issue where the request would not be made to the server
- Fixed an issue where there would be an endless loop caused when getting save files

## Server Information
- Fixed an issue where server information will not be saved

## Main Client Save File Related Issues
- Fixed an issue where the user will not be prompted to create a new save file if the server doesn't have one
- Fixed issues causing save files to not be parsed properly

## Textbox Component
- Fixed an issue where the textboxes will show button prompts regardless of the settings 
- Added quit functionality to quit the textbox

## Dashboard
- Fixed an issue where the text will overlap
- Added the quit button toolip
- Fixed an issue where pressing any key will close the app (Although this fix is implemented poorly)

# Remaining Issues
## Save File Issues
- The app cannot parse save files from the server after being decrypted

***This issue is now fixed, see BugFix1.5.md***
