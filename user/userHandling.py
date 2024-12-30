from .passwordValidator import PasswordValidator
import json
import os

class UserHandler:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file
        self.password_validator = PasswordValidator()
        self._ensure_data_file()

    def _ensure_data_file(self):
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)

    def create_user(self):
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
                
            is_valid, errors = self.password_validator.validate(password)
            if is_valid:
                break
            else:
                print("\nPassword errors:")
                for error in errors:
                    print(f"- {error}")
                
            if input("\nTry again? (y/n): ").lower() != 'y':
                return None
        
        return {
            "email": email,
            "username": username,
            "password": password  # In real app, hash this before storing
        }

    def verify_login(self, username, password):
        with open(self.data_file, 'r') as f:
            users = json.load(f)
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False