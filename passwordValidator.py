import re
from typing import Tuple, List

class PasswordValidator:
    def __init__(self):
        self.special_chars = '!@#$%^&*()-_=+[]{}|;:,.<>?/~`'
        self.min_length = 8
        self.max_length = 128  # Adding max length for security
        self.max_repeated_chars = 3  # Maximum times a character can be repeated consecutively
        
    def validate(self, password: str) -> Tuple[bool, List[str]]:
        
        errors = []
        
        # Basic requirements
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters")
        if len(password) > self.max_length:
            errors.append(f"Password must not exceed {self.max_length} characters")
        if not any(char.isupper() for char in password):
            errors.append("Must contain uppercase letter")
        if not any(char.islower() for char in password):
            errors.append("Must contain lowercase letter")
        if not any(char.isdigit() for char in password):
            errors.append("Must contain number")
        if not any(char in self.special_chars for char in password):
            errors.append("Must contain special character")
        if any(char.isspace() for char in password):
            errors.append("Must not contain whitespace characters")
            
        # Advanced security checks
        # Check for repeated characters
        for i in range(len(password) - self.max_repeated_chars + 1):
            if all(password[i] == password[j] for j in range(i, i + self.max_repeated_chars)):
                errors.append(f"Cannot repeat the same character more than {self.max_repeated_chars} times")
                break
                
        # Check for common patterns
        common_patterns = [
            r'12345', r'qwerty', r'password', r'admin', r'letmein',
            r'welcome', r'abc123', r'\d{6,}',  # 6 or more consecutive numbers
        ]
        # idk might use seclists for this, but would take too long?
        # not sure which one to use
        for pattern in common_patterns:
            if re.search(pattern, password.lower()):
                errors.append("Contains common password pattern")
                break
                
        # Check for keyboard patterns
        keyboard_rows = [
            'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
            '1234567890'
        ]
        for row in keyboard_rows:
            for i in range(len(row) - 3):
                if row[i:i+4].lower() in password.lower():
                    errors.append("Contains keyboard pattern")
                    break
        
        return (len(errors) == 0, errors)
    
    def suggest_password(self) -> str:
        import random
        import string
        
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = self.special_chars
        
        # Ensure at least one of each required character type
        password = [
            random.choice(uppercase),
            random.choice(lowercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Add additional random characters
        length = random.randint(self.min_length + 4, min(self.min_length + 8, 16))
        all_chars = lowercase + uppercase + digits + special
        password.extend(random.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle the password
        random.shuffle(password)
        return ''.join(password)