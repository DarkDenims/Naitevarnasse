import os
import base64
import json
import logging
import bcrypt
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
from .passwordValidator import PasswordValidator
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class UserHandling:
    def __init__(self, users_file: str = 'users.json'):
        """Initialize UserHandling with configuration."""
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
        """Initialize the users file if it doesn't exist."""
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({
                    "users": {},
                    "failed_attempts": {},
                    "lockouts": {}
                }, f, indent=4)

    def _generate_master_key(self, password: str) -> str:
        """Generate a master key from password using PBKDF2."""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return f"{base64.b64encode(salt).decode()}:{key.decode()}"

    def _check_lockout(self, username: str) -> Tuple[bool, Optional[timedelta]]:
        """Check if a user is locked out and return remaining lockout time."""
        try:
            with open(self.users_file, 'r') as f:
                data = json.load(f)
            
            lockouts = data.get("lockouts", {})
            if username in lockouts:
                lockout_time = datetime.fromisoformat(lockouts[username])
                if datetime.now() < lockout_time:
                    remaining = lockout_time - datetime.now()
                    return True, remaining
                else:
                    # Lockout expired, remove it
                    del lockouts[username]
                    data["lockouts"] = lockouts
                    with open(self.users_file, 'w') as f:
                        json.dump(data, f, indent=4)
            
            return False, None
            
        except Exception as e:
            logging.error(f"Error checking lockout: {str(e)}")
            return False, None

    def _record_failed_attempt(self, username: str) -> None:
        """Record a failed login attempt and implement lockout if necessary."""
        try:
            with open(self.users_file, 'r') as f:
                data = json.load(f)
            
            failed_attempts = data.get("failed_attempts", {})
            failed_attempts[username] = failed_attempts.get(username, 0) + 1
            
            if failed_attempts[username] >= self.max_login_attempts:
                lockout_time = datetime.now() + self.lockout_duration
                data["lockouts"] = data.get("lockouts", {})
                data["lockouts"][username] = lockout_time.isoformat()
                failed_attempts[username] = 0  # Reset counter
            
            data["failed_attempts"] = failed_attempts
            
            with open(self.users_file, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            logging.error(f"Error recording failed attempt: {str(e)}")

    def _reset_failed_attempts(self, username: str) -> None:
        """Reset failed login attempts after successful login."""
        try:
            with open(self.users_file, 'r') as f:
                data = json.load(f)
            
            if username in data.get("failed_attempts", {}):
                data["failed_attempts"][username] = 0
                
            with open(self.users_file, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            logging.error(f"Error resetting failed attempts: {str(e)}")

    def create_user(self) -> Optional[Dict]:
        """Create a new user with validated credentials."""
        print("\n=== User Registration ===")
        try:
            # Username validation
            username = input("Username (min 3 characters): ").strip()
            if len(username) < 3:
                print("Username must be at least 3 characters!")
                return None

            with open(self.users_file, 'r') as f:
                data = json.load(f)

            if username in data["users"]:
                print("Username already exists!")
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
            
            data["users"][username] = {
                "master_key": master_key,
                "created_at": datetime.now().isoformat(),
                "last_login": None
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
        """Verify login credentials with lockout handling."""
        try:
            # Check for lockout
            is_locked, remaining_time = self._check_lockout(username)
            if is_locked:
                print(f"Account is locked. Try again in {remaining_time.seconds // 60} minutes.")
                return None

            with open(self.users_file, 'r') as f:
                data = json.load(f)

            if username not in data["users"]:
                self._record_failed_attempt(username)
                return None

            stored_key = data["users"][username]["master_key"]
            salt, key = stored_key.split(':')
            
            # Verify password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=base64.b64decode(salt),
                iterations=100000,
            )
            
            try:
                test_key = base64.urlsafe_b64encode(
                    kdf.derive(password.encode())
                ).decode()
                
                if test_key == key:
                    # Successful login
                    self._reset_failed_attempts(username)
                    
                    # Update last login time
                    data["users"][username]["last_login"] = datetime.now().isoformat()
                    with open(self.users_file, 'w') as f:
                        json.dump(data, f, indent=4)
                    
                    logging.info(f"Successful login: {username}")
                    return key
                
            except Exception:
                pass
            
            # Failed login
            self._record_failed_attempt(username)
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