class PasswordValidator:
    def __init__(self):
        self.special_chars = '!@#$%^&*()-_=+[]{}|;:,.<>?/~`'
        self.min_length = 8

    def validate(self, password):
        errors = []
        
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters")
        if not any(char.isupper() for char in password):
            errors.append("Must contain uppercase letter")
        if not any(char.islower() for char in password):
            errors.append("Must contain lowercase letter")
        if not any(char.isdigit() for char in password):
            errors.append("Must contain number")
        if not any(char in self.special_chars for char in password):
            errors.append("Must contain special character")
        
        return (len(errors) == 0, errors)
    
    # okay this is weird cause the password validator
    # is not validating the passwords at all LMAO