import bcrypt
import json
import os
import uuid
from .passwordValidator import PasswordValidator

class UserHandling:
    def __init__(self, dataFile='data.json'):
        self.dataFile = dataFile
        self.passwordValidator = PasswordValidator()
        self._ensureDataFile()

    def _ensureDataFile(self):
        if not os.path.exists(self.dataFile):
            with open(self.dataFile, 'w') as f:
                json.dump({"users": []}, f)

    def createUser(self):
        try:
            print("\n=== User Registration ===")
            email = input('Enter email: ')
            username = input('Enter username: ')

            self._ensureDataFile()
            # sanity check

            while True:
                print("\nPassword requirements:")
                print("- At least 8 characters")
                print("- Uppercase and lowercase letters")
                print("- Numbers and special characters")
                
                password = input('Enter password: ')
                confirmPassword = input('Confirm password: ')

                if password != confirmPassword:
                    print("Passwords don't match!")
                    continue

                is_valid, errors = self.passwordValidator.validate(password)
                if is_valid:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                    with open(self.dataFile, 'r') as f:
                        data = json.load(f)

                    newUser = {
                        "id": str(uuid.uuid4()),
                        "email": email,
                        "username": username,
                        "password": hashed_password.decode('utf-8')  # store the hashed password as a string
                    }

                    data["users"].append(newUser)

                    with open(self.dataFile, 'w') as f:
                        json.dump(data, f, indent=4)
                    
                    print(f"User '{username}' created successfully!")
                    return newUser
                else:
                    print("\nPassword does not meet requirements!")
                    print("Errors:", errors)

                if input("\nTry again? (y/n): ").lower() != 'y':
                    return None

        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def verifyLogin(self, username, password):
        try:
            with open(self.dataFile, 'r') as f:
                data = json.load(f)

            for user in data["users"]:
                if user["username"] == username:
                    if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                        print(f"Login successful for {username}!")
                        return True
            print("Invalid username or password.")
            return False

        except Exception as e:
            print(f"Login error: {e}")
            return 
    
    def emailTaken(self, email):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        for user in data.get("users", []):
            if user["email"] == email:
                return True
        return False
    
    def usernameTaken(self, username):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        for user in data.get("users", []):
            if user["username"] == username:
                return True
        return False


# Problem 1: multiple users with same username and email
# Problem 2: storing passwords in plaintext(fix when i have GUI?)
# Problem 3: I still don't have a way to store the credentials according
# to the user. I need to figure out a way to do that.