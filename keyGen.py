from cryptography.fernet import Fernet
from datetime import datetime
import base64
import secrets
import json
import os

class KeyManager:
    def __init__(self, storage_path='./rawdata.json'):
        self.storage_path = storage_path

    def create_key(self, user_id):
        random_bytes = secrets.token_bytes(32)
        timestamp = datetime.now().isoformat()
        combined = f"{user_id}:{timestamp}".encode() + random_bytes
        key = base64.urlsafe_b64encode(combined[:32])
        
        return {
            'raw_key': combined,
            'encoded_key': key.decode('utf-8'),
            'created_at': timestamp
        }

    def store_key(self, user_id):
        try:
            key_data = self.create_key(user_id)
            
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            if 'keys' not in data:
                data['keys'] = {}
                
            data['keys'][user_id] = {
                'key': key_data['encoded_key'],
                'created_at': key_data['created_at']
            }
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=4)
                
            return True
            
        except Exception as e:
            print(f"Error storing key: {e}")
            return False
            
    def get_key(self, user_id):
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                
            return data['keys'].get(user_id)
        except Exception as e:
            print(f"Error retrieving key: {e}")
            return None

if __name__ == "__main__":
    key_manager = KeyManager()
    key_manager.store_key("123")
    stored_key = key_manager.get_key("123")
    print(f"Stored key: {stored_key}")

# I can now create a key but only for one user, I can also store the key and retrieve it
# Been thinking about how to properly use these keys