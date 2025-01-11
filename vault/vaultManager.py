import bcrypt
import json
import logging
import os
from typing import Dict
from tabulate import tabulate
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class VaultManager:
    def __init__(self, master_key: str, username: str, base_dir: str = 'userApps'):
        """
        Initialize VaultManager with user-specific vault file in userApps directory.
        
        Args:
            master_key (str): User's master key for encryption
            username (str): Username to create user-specific vault
            base_dir (str): Base directory for user vaults (default: 'userApps')
        """
        self.username = username
        self.base_dir = base_dir
        self.user_dir = os.path.join(self.base_dir, username)
        self.data_file = os.path.join(self.user_dir, 'vault.json')
        
        # Initialize encryption
        self.fernet = self._initialize_encryption(master_key)
        
        # Set up logging with user-specific log file
        self.log_file = os.path.join(self.user_dir, 'vault.log')
        self._setup_logging()
        
        # Initialize directory structure and vault
        self._initialize_directory_structure()
        self._initialize_vault()

    def _setup_logging(self) -> None:
        """Set up logging with user-specific log file."""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _initialize_directory_structure(self) -> None:
        """Create necessary directory structure for user vault."""
        try:
            # Create base directory if it doesn't exist
            if not os.path.exists(self.base_dir):
                os.makedirs(self.base_dir)
                logging.info(f"Created base directory: {self.base_dir}")

            # Create user-specific directory if it doesn't exist
            if not os.path.exists(self.user_dir):
                os.makedirs(self.user_dir)
                logging.info(f"Created user directory for {self.username}")
                
        except Exception as e:
            logging.error(f"Error creating directory structure: {str(e)}")
            raise

    def _initialize_encryption(self, master_key: str) -> Fernet:
        """Initialize encryption with user's master key."""
        salt = b'salt_'  # In production, use a secure random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        return Fernet(key)

    def _initialize_vault(self) -> None:
        """Initialize user's vault file if it doesn't exist."""
        try:
            if not os.path.exists(self.data_file):
                with open(self.data_file, 'w') as file:
                    json.dump({"credentials": []}, file)
                logging.info(f"Created new vault file for user {self.username}")
            else:
                # Verify file is readable and has valid JSON
                with open(self.data_file, 'r') as file:
                    json.load(file)
                    
        except Exception as e:
            logging.error(f"Error initializing vault: {str(e)}")
            raise

    def display_vault(self, mask_passwords: bool = True) -> None:
        """Display vault contents with optional password masking."""
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            
            credentials = data.get("credentials", [])
            
            headers = ["Service", "Username", "Password", "Email"]
            rows = []
            
            for cred in credentials:
                password_display = "********" if mask_passwords else \
                                 self.fernet.decrypt(cred["password"].encode()).decode()
                rows.append([
                    cred["service"],
                    cred["username"],
                    password_display,
                    self.fernet.decrypt(cred["email"].encode()).decode()
                ])
            
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        except Exception as e:
            logging.error(f"Error displaying vault: {str(e)}")
            raise

    def add_credentials(self, username: str, password: str, email: str, service: str) -> bool:
        """Add new credentials to the user's vault."""
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            
            encrypted_password = self.fernet.encrypt(password.encode()).decode()
            encrypted_email = self.fernet.encrypt(email.encode()).decode()
            
            data["credentials"].append({
                "service": service,
                "username": username,
                "password": encrypted_password,
                "email": encrypted_email
            })
            
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
            
            logging.info(f"Added new credentials for service: {service}")
            return True
            
        except Exception as e:
            logging.error(f"Error adding credentials: {str(e)}")
            return False

    def delete_credentials(self, service: str, username: str) -> bool:
        """Delete credentials from the user's vault."""
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
            
            initial_length = len(data["credentials"])
            data["credentials"] = [
                cred for cred in data["credentials"]
                if not (cred["service"] == service and cred["username"] == username)
            ]
            
            if len(data["credentials"]) < initial_length:
                with open(self.data_file, 'w') as file:
                    json.dump(data, file, indent=4)
                logging.info(f"Deleted credentials for service: {service}")
                return True
            return False
            
        except Exception as e:
            logging.error(f"Error deleting credentials: {str(e)}")
            return False

# Gonna transfer to GraphQL