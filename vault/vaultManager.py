import bcrypt
import json
from tabulate import tabulate
import logging
from typing import Dict, List, Optional
import re
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordValidator:
    @staticmethod
    def is_strong_password(password: str) -> bool:
        """
        Validate password strength using following rules:
        - Minimum 12 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
        if len(password) < 12:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))

class Encryption:
    def __init__(self, master_key: str):
        """Initialize encryption with a master key."""
        salt = b'salt_'  # In production, use a secure random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt string data."""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt encrypted data."""
        return self.fernet.decrypt(encrypted_data.encode()).decode()

class VaultManager:
    def __init__(self, master_key: str, data_file: str = 'vault.json'):
        """
        Initialize VaultManager with master key and data file path.
        
        Args:
            master_key: Master encryption key for the vault
            data_file: Path to the JSON file storing vault data
        """
        self.data_file = data_file
        self.encryption = Encryption(master_key)
        self.validator = PasswordValidator()
        
        # Set up logging
        logging.basicConfig(
            filename='vault.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Initialize data file if it doesn't exist
        try:
            with open(self.data_file, 'r') as file:
                json.load(file)
        except FileNotFoundError:
            with open(self.data_file, 'w') as file:
                json.dump({"users": []}, file)

    def _load_data(self) -> Dict:
        """Load data from JSON file with error handling."""
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Error loading data: {str(e)}")
            raise ValueError("Failed to load vault data")

    def _save_data(self, data: Dict) -> None:
        """Save data to JSON file with error handling."""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            logging.error(f"Error saving data: {str(e)}")
            raise ValueError("Failed to save vault data")

    def display_vault(self, mask_passwords: bool = True) -> None:
        """
        Display vault contents in a formatted table.
        
        Args:
            mask_passwords: If True, masks passwords in display
        """
        try:
            data = self._load_data()
            users = data.get("users", [])
            
            headers = ["ID", "Username", "Password", "Email"]
            rows = []
            
            for i, user in enumerate(users, 1):
                password_display = "********" if mask_passwords else self.encryption.decrypt(user["password"])
                rows.append([
                    i,
                    user["username"],
                    password_display,
                    self.encryption.decrypt(user["email"])
                ])
            
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        except Exception as e:
            logging.error(f"Error displaying vault: {str(e)}")
            raise

    def add_credentials(self, username: str, password: str, email: str) -> bool:
        """
        Add new credentials to the vault with validation.
        
        Args:
            username: Username for the new entry
            password: Password for the new entry
            email: Email for the new entry
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate inputs
            if not username or len(username) < 3:
                raise ValueError("Username must be at least 3 characters long")
            
            if not self.validator.is_strong_password(password):
                raise ValueError("Password does not meet security requirements")
            
            if not self.validator.is_valid_email(email):
                raise ValueError("Invalid email format")
            
            # Check for duplicate username
            data = self._load_data()
            if any(user["username"] == username for user in data["users"]):
                raise ValueError("Username already exists")
            
            # Hash password and encrypt sensitive data
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            encrypted_password = self.encryption.encrypt(hashed_password.decode('utf-8'))
            encrypted_email = self.encryption.encrypt(email)
            
            # Add new entry
            data["users"].append({
                "username": username,
                "password": encrypted_password,
                "email": encrypted_email,
            })
            
            self._save_data(data)
            logging.info(f"Added new credentials for user: {username}")
            return True
            
        except Exception as e:
            logging.error(f"Error adding credentials: {str(e)}")
            raise

    def verify_password(self, username: str, input_password: str) -> bool:
        """
        Verify password for given username.
        
        Args:
            username: Username to verify
            input_password: Password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            data = self._load_data()
            for user in data.get("users", []):
                if user["username"] == username:
                    stored_password = self.encryption.decrypt(user["password"])
                    return bcrypt.checkpw(
                        input_password.encode('utf-8'),
                        stored_password.encode('utf-8')
                    )
            return False
        except Exception as e:
            logging.error(f"Error verifying password: {str(e)}")
            raise

    def delete_credentials(self, username: str) -> bool:
        """
        Delete credentials for given username.
        
        Args:
            username: Username to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        try:
            data = self._load_data()
            initial_length = len(data["users"])
            data["users"] = [user for user in data["users"] if user["username"] != username]
            
            if len(data["users"]) < initial_length:
                self._save_data(data)
                logging.info(f"Deleted credentials for user: {username}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error deleting credentials: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    try:
        # Initialize vault with a master key
        vault = VaultManager("your-secure-master-key")
        
        # Add new credentials
        vault.add_credentials(
            "john_doe",
            "SecureP@ssw0rd123!",
            "john@example.com"
        )
        
        # Display vault contents
        vault.display_vault()
        
        # Verify password
        is_valid = vault.verify_password("john_doe", "SecureP@ssw0rd123!")
        print(f"Password verification result: {is_valid}")
        
        # Delete credentials
        vault.delete_credentials("john_doe")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Main execution error: {str(e)}")