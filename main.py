from user.userHandling import UserHandler
from vault.vaultManager import VaultManager

class PasswordManager:
    def __init__(self):
        self.user_handler = UserHandler()
        self.vault_manager = VaultManager()
        self.logged_in = False

    def main_menu(self):
        while True:
            print("\n=== Password Manager ===")
            print("[S]ignup")
            print("[L]ogin")
            print("[E]xit")
            
            choice = input("Choice: ").lower()
            
            if choice == 'l':
                self.login()
            elif choice == 's':
                self.signup()
            elif choice == 'e':
                print("Exiting...")
                break
            else:
                print("Invalid choice!")

    def login(self):
        print("\n=== Login ===")
        attempts = 3
        while attempts > 0:
            username = input("Username: ")
            password = input("Password: ")
            
            if self.userHandling.verify_login(username, password):
                self.logged_in = True
                self.vault_menu()
                break
            
            attempts -= 1
            print(f"Invalid credentials! {attempts} attempts remaining.")

    def signup(self):
        user_data = self.userHandling.create_user()
        if user_data:
            # Save user data
            print("Registration successful!")
        else:
            print("Registration cancelled.")

    def vault_menu(self):
        while self.logged_in:
            print("\n=== Vault Menu ===")
            print("[D]isplay Vault")
            print("[N]ew Credentials")
            print("[A]rchive Credentials")
            print("[L]ogout")
            print("[E]xit")
            
            choice = input("Choice: ").lower()
            
            if choice == 'd':
                self.vaultManager.display_vault()
            elif choice == 'n':
                self.add_new_credentials()
            elif choice == 'a':
                self.archive_credentials()
            elif choice == 'l':
                self.logged_in = False
            elif choice == 'e':
                self.logged_in = False
                exit()
            else:
                print("Invalid choice!")

    def add_new_credentials(self):
        print("\n=== Add New Credentials ===")
        # Implement credential addition
        pass

    def archive_credentials(self):
        print("\n=== Archive Credentials ===")
        # Implement archive functionality
        pass

if __name__ == "__main__":
    manager = PasswordManager()
    manager.main_menu()