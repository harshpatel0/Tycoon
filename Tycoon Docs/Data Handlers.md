# Data Handlers
Modules used to handle data
- **Backend Handler** `modules/datahandlers/backendhandler.py` - Deals with any server related tasks such as encrypting or uploading and downloading and decrypting save files
- **Data Handler** `modules/datahandlers/datahandler.py` - Deals with adding or subtracting values, basically anything to do with the values inside the save data 
## Save Files
Save Files are stored as basic JSON files and are encrypted before being sent to the server

```
{
	"name": "John Doe",
	"empire-name": "Acme Inc."
	"money": 10000,
	"properties": ["Test Joint", "Acme Building"]
}
```

All the data is handled by a `datahandler.py` file and other files can retrieve data from it and any function that requires changing the save data has to be done through the `datahandler.py` file

### Methods in the datahandler.py file
- `save_file_parser(self)` - Puts all the data into the class variables list so its easy for other files to get data from it
	- **This method is called each time a save is done and when the game first loads**
- `save(self)` - Takes all the data and puts into the raw JSON save data before encrypting and uploading it
	- `upload(self)`  - Requires the `backendhandler.py` file. Uses its build in methods to encrypt the save file and uploads it to the server 
		- `backendhander.py` relies on the `requesthandler.py` file to upload the file
		**This method is called each time a save is done**
- `remove_money(self, amount)` - Removes money then saves the file
- `add_money(self, amount)` - Adds money then saves the file
- `remove_property(self, property_name)`
- `add_property(self, property_name)`
- `change_name(self, new_name)`
- `change_empire_name(self, new_name)`
- `handle_all_buy(property_name)` - Handles all the functions related to buying properties
	- Getting the value of the property
	- Removing the money
	- Adding the property
	- Saving the changes
- `handle_all_sell(property_name)` - Handles all the functions related to selling properties
	- Getting the value of the property
	- Adding the money
	- Removing the property
	- Saving the changes
- `check_buy_requirements(self, property_name, price)` - Checks if they have enough money to buy a property and if they own it or not 
- `check_sell_requirements(self, property_name)` - Checks if they have  they own the property or not 

