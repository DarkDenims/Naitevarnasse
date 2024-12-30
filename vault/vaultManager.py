from cryptography.fernet import Fernet
import json
from tabulate import tabulate

class VaultManager:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file

    def display_vault(self):
        with open(self.data_file, 'r') as file:
            data = json.load(file)
        
        headers = ["Username", "Password", "Email", "Website"]
        rows = [[d["username"], d["password"], d["email"], d["website"]] 
               for d in data]
        
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def add_credentials(self, username, password, email, website):
        with open(self.data_file, 'r+') as file:
            data = json.load(file)
            data.append({
                "username": username,
                "password": password,
                "email": email,
                "website": website
            })
            file.seek(0)
            json.dump(data, file, indent=4)