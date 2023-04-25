import hashlib
import json

class AccountsHandler:
    accounts = {}

    def __init__(self, accounts_file_path):
        self.accounts_file_path = accounts_file_path
        self.load_accounts()

    def load_accounts(self):
        with open(f'{self.accounts_file_path}' ,'r') as accountsfile:
            self.accounts = json.load(accountsfile)

    def save_accounts(self):
        with open(f'{self.accounts_file_path}', 'w') as accountsfile:
            json.dump(self.accounts)

    def add_account(self, username, gameusername, password):
        # Check if the account already exists

        if username in self.accounts:
            return "ALREADYEXISTS"

        account_details = {
                'username': {
                    'gameusername': gameusername,
                    'password': password
                    }
                }
        self.accounts.update(account_details)
    
    def authorise_login(self, username, password):
        """
        The password received must be hashed
        """
        try:
            account = self.accounts['username']
        except KeyError:
            return "NOTFOUND"

        account_password_on_server = account['password']
        if account_password_on_server == password:
            return account['gameusername']
        else:
            return "WRONGPASSWORD"
