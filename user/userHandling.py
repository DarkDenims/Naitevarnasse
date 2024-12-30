from .passwordValidator import PasswordValidator
import json
import os

class UserHandler:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file
        self.passwordValidator = PasswordValidator()
        self._ensure_data_file()

    def _ensure_data_file(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)

    def create_user(self):
        try:
            print("\n=== User Registration ===")
            email = input('Enter email: ')
            username = input('Enter username: ')
            
            while True:
                print("\nPassword requirements:")
                print("- At least 8 characters")
                print("- Uppercase and lowercase letters")
                print("- Numbers and special characters")
                
                password = input('Enter password: ')
                confirm_password = input('Confirm password: ')
                
                if password != confirm_password:
                    print("Passwords don't match!")
                    continue

                if self.passwordValidator.validate(password):
                    # Read existing data
                    if os.path.exists(self.data_file):
                        with open(self.data_file, 'r') as f:
                            try:
                                data = json.load(f)
                            except json.JSONDecodeError:
                                data = {"users": []}
                    else:
                        data = {"users": []}

                    # Add new user
                    new_user = {
                        "email": email,
                        "username": username,
                        "password": password  # In production, hash this password
                    }

                    if "users" not in data:
                        data["users"] = []
                    
                    data["users"].append(new_user)

                    # Write back to file
                    with open(self.data_file, 'w') as f:
                        json.dump(data, f, indent=4)
                    
                    return new_user
                else:
                    print("\nPassword does not meet requirements!")
                    
                if input("\nTry again? (y/n): ").lower() != 'y':
                    return None
                    
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def verify_login(self, username, password):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
            if "users" in data:
                for user in data["users"]:
                    if user["username"] == username and user["password"] == password:
                        return True
            return False
            
        except Exception as e:
            print(f"Login error: {e}")
            return False