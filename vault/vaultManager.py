import bcrypt
import json
from tabulate import tabulate

class VaultManager:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file

    def displayVault(self):
        with open(self.data_file, 'r') as file:
            data = json.load(file)
        
        users = data.get("users", [])
        
        headers = ["ID", "Username", "Password", "Email"]
        rows = [[
                d.get("id", ""),
                d.get("username", ""),
                d.get("password", ""),
                d.get("email", "")
            ] for d in users]

        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def addNewCredentials(self, username, password, email):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        with open(self.data_file, 'r+') as file:
            data = json.load(file)
            data['users'].append({
                "username": username,
                "password": hashed_password.decode('utf-8'),
                "email": email,
            })
            file.seek(0)
            json.dump(data, file, indent=4)

    def verifyPassword(self, username, input_password):
        with open(self.data_file, 'r') as file:
            data = json.load(file)
            for user in data.get("users", []):
                if user["username"] == username:
                    stored_password = user.get("password", "")
                    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password.encode('utf-8'))
        return False


    # the problem here is that we need to create new files for each users
    # as the data shouldn't be shared throughout all users