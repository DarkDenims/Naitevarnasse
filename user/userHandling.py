import os
import base64
import json
import logging
from typing import Optional, Dict
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class UserHandling:
    def __init__(self, users_file: str = 'users.json'):
        self.users_file = users_file
        self._initialize_users_file()
        
        logging.basicConfig(
            filename='users.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _initialize_users_file(self) -> None:
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({"users": {}}, f)

    def _generate_master_key(self, password: str) -> str:
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return f"{base64.b64encode(salt).decode()}:{key.decode()}"

    def _verify_master_key(self, password: str, stored_key: str) -> bool:
        try:
            salt, key = stored_key.split(':')
            salt = base64.b64decode(salt)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            new_key = base64.urlsafe_b64encode(kdf.derive(password.encode())).decode()
            return new_key == key
        except Exception as e:
            logging.error(f"Error verifying master key: {str(e)}")
            return False

    def create_user(self) -> Optional[Dict]:
        print("\n=== User Registration ===")
        try:
            username = input("Username (min 3 characters): ").strip()
            if len(username) < 3:
                print("Username must be at least 3 characters!")
                return None

            with open(self.users_file, 'r') as f:
                data = json.load(f)

            if username in data["users"]:
                print("Username already exists!")
                return None

            password = input("Password (min 12 characters, include upper, lower, number, special): ")
            if len(password) < 12:
                print("Password too short!")
                return None

            confirm_password = input("Confirm password: ")
            if password != confirm_password:
                print("Passwords don't match!")
                return None

            master_key = self._generate_master_key(password)
            
            data["users"][username] = {
                "master_key": master_key
            }
            
            with open(self.users_file, 'w') as f:
                json.dump(data, f, indent=4)

            logging.info(f"Created new user: {username}")
            return {"username": username, "master_key": master_key}

        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            print("An error occurred during registration.")
            return None

    def verify_login(self, username: str, password: str) -> Optional[str]:
        try:
            with open(self.users_file, 'r') as f:
                data = json.load(f)

            if username not in data["users"]:
                return None

            stored_key = data["users"][username]["master_key"]
            if self._verify_master_key(password, stored_key):
                logging.info(f"Successful login: {username}")
                return stored_key.split(':')[1]
            
            logging.warning(f"Failed login attempt for user: {username}")
            return None

        except Exception as e:
            logging.error(f"Error during login verification: {str(e)}")
            return None

# Problem 1: multiple users with same username and email
# Problem 2: storing passwords in plaintext(fix when i have GUI?)
# Problem 3: I still don't have a way to store the credentials according
# to the user. I need to figure out a way to do that.


# i was wrong i dont need to make a new instance per User that's for the Cloud version
# what im trying to create is a standalone version in the first place