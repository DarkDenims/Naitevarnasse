from cryptography.fernet import Fernet
import json
from tabulate import tabulate

class VaultManager:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file

    def display_vault(self):
        with open(self.data_file, 'r') as file:
            data = json.load(file)
        
        users = data.get("users", [])
        
        headers = ["Username", "Password", "Email"]
        rows = [[
                d.get("username", ""),
                d.get("password", ""),
                d.get("email", "")
            ] for d in users]

        
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def add_credentials(self, username, password, email):
        with open(self.data_file, 'r+') as file:
            data = json.load(file)
            data.append({
                "username": username,
                "password": password,
                "email": email,
            })
            file.seek(0)
            json.dump(data, file, indent=4)

    # the problem here is that we need to create new files for each users
    # as the data shouldn't be shared throughout all users