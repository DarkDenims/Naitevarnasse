import os
import time
import base64
import json
import logging
import bcrypt
import re
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
from .passwordValidator import PasswordValidator
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class UserHandling:
    def __init__(self, users_file: str = 'users.json'):
        self.users_file = users_file
        self.password_validator = PasswordValidator()
        self.max_login_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
        
        # Set up logging
        logging.basicConfig(
            filename='users.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self._initialize_users_file()
    
    def _initialize_users_file(self) -> None:
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({
                    "users": {},
                    "email_index": {},  # New index to track email usage
                    "failed_attempts": {},
                    "lockouts": {}
                }, f, indent=4)

    def _is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _is_email_taken(self, email: str) -> bool:
        try:
            with open(self.users_file, 'r') as f:
                data = json.load(f)
            return email.lower() in data.get("email_index", {})
        except Exception as e:
            logging.error(f"Error checking email: {str(e)}")
            return False

    def _normalize_username(self, username: str) -> str:
        return username.strip().lower()
    
    def clear_screen():
        time.sleep(5)
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def create_user(self) -> Optional[Dict]:
        print("\n=== User Registration ===")
        try:
            # Username validation with normalization
            username = input("Username (min 3 characters): ").strip()
            normalized_username = self._normalize_username(username)
            
            if len(normalized_username) < 3:
                print("Username must be at least 3 characters!")
                return None

            # Email validation
            while True:
                email = input("Email address: ").strip().lower()
                if not self._is_valid_email(email):
                    print("Invalid email format!")
                    if input("Try again? (y/n): ").lower() != 'y':
                        return None
                    continue
                
                if self._is_email_taken(email):
                    print("Email address is already registered!")
                    if input("Try again? (y/n): ").lower() != 'y':
                        return None
                    continue
                break

            with open(self.users_file, 'r') as f:
                data = json.load(f)

            # Check for existing username (case-insensitive)
            if any(self._normalize_username(existing_user) == normalized_username 
                  for existing_user in data["users"]):
                print("Username already exists!")    
                time.sleep(2.5) # wait for 2.5 seconds or 5 seconds?
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')
                # might work?
                return None

            # Password validation
            while True:
                password = input("Password: ")
                is_valid, errors = self.password_validator.validate(password)
                
                if not is_valid:
                    print("Password does not meet requirements:")
                    for error in errors:
                        print(f"- {error}")
                    suggestion = self.password_validator.suggest_password()
                    print(f"\nSuggested password: {suggestion}")
                    if input("Try again? (y/n): ").lower() != 'y':
                        return None
                    continue
                
                confirm_password = input("Confirm password: ")
                if password != confirm_password:
                    print("Passwords don't match!")
                    if input("Try again? (y/n): ").lower() != 'y':
                        return None
                    continue
                    
                break

            # Generate master key and save user
            master_key = self._generate_master_key(password)
            
            # Update user data
            data["users"][username] = {
                "master_key": master_key,
                "email": email,
                "created_at": datetime.now().isoformat(),
                "last_login": None
            }
            
            # Update email index
            data["email_index"] = data.get("email_index", {})
            data["email_index"][email] = username
            
            with open(self.users_file, 'w') as f:
                json.dump(data, f, indent=4)

            logging.info(f"Created new user: {username} with email: {email}")
            return {"username": username, "email": email, "master_key": master_key}

        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            print("An error occurred during registration.")
            return None
        
        
# Problem 1: multiple users with same username and email - fixed?
# Problem 2: storing passwords in plaintext(fix when i have GUI?)
# Problem 3: I still don't have a way to store the credentials according
# to the user. I need to figure out a way to do that.
# Problem 4: I need to figure out a way to store the master key for each user

# i was wrong i dont need to make a new instance per User that's for the Cloud version
# what im trying to create is a standalone version in the first place