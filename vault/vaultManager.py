import bcrypt
import json
import logging
from typing import Dict
from tabulate import tabulate
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class VaultManager:
    def __init__(self, master_key: str, data_file: str = 'vault.json'):
        self.data_file = data_file
        self.fernet = self._initialize_encryption(master_key)
        
        logging.basicConfig(
            filename='vault.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self._initialize_vault()

    def _initialize_encryption(self, master_key: str) -> Fernet:
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
        try:
            with open(self.data_file, 'r') as file:
                json.load(file)
        except FileNotFoundError:
            with open(self.data_file, 'w') as file:
                json.dump({"credentials": []}, file)

    def display_vault(self, mask_passwords: bool = True) -> None:
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