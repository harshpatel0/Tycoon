import json

# Game Settings
# These don't work and soon they will be moved to another file
enable_button_tooltips = False
enable_autoconnect = False
auto_connect_to_server = "www.example.com"
enable_logging = False

# Debug Switches
debug_skip_ip = True 
debug_skip_new_save_file_message = True
debug_skip_name_when_creating_new_save_files = True
debug_skip_empire_name_when_creating_new_save_files = True
debug_enable_wip_features = True
debug_ignore_settings_file = False # Unused


# Debug Options
debug_use_ip = "127.0.0.1:8000"
debug_create_save_file_with_name = "Test"
debug_create_save_file_with_empire_name = "Test"

with open("settings.jsonc", 'r') as settingsfile:
  settings = json.load(settingsfile)

print(settings)