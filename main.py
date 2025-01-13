from user.userHandling import UserHandling
from vault.vaultManager import VaultManager

class PasswordManager:
    def __init__(self):
        self.user_handling = UserHandling()
        self.vault_manager = None
        self.logged_in = False
        self.current_user = None

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
            
            master_key = self.user_handling.verify_login(username, password)
            if master_key:
                self.logged_in = True
                self.current_user = username
                self.vault_manager = VaultManager(master_key, f'vault_{username}.json')
                self.vault_menu()
                break
            
            attempts -= 1
            print(f"Invalid credentials! {attempts} attempts remaining.")

    def signup(self):
        user_data = self.user_handling.create_user()
        if user_data:
            print("Registration successful! Please login to continue.")
        else:
            print("Registration cancelled.")

    def vault_menu(self):
        while self.logged_in:
            print(f"\n=== Vault Menu ({self.current_user}) ===")
            print("[D]isplay Vault")
            print("[A]dd New Credentials")
            print("[R]emove Credentials")
            print("[L]ogout")
            print("[E]xit")
            
            choice = input("Choice: ").lower()
            
            try:
                if choice == 'd':
                    self.vault_manager.display_vault()
                elif choice == 'a':
                    self.add_new_credentials()
                elif choice == 'r':
                    self.remove_credentials()
                elif choice == 'l':
                    self.logged_in = False
                    self.current_user = None
                    self.vault_manager = None
                elif choice == 'e':
                    self.logged_in = False
                    exit()
                else:
                    print("Invalid choice!")
            except Exception as e:
                print(f"Error: {str(e)}")
                logging.error(f"Error in vault menu: {str(e)}")

    def add_new_credentials(self):
        print("\n=== Add New Credentials ===")
        try:
            service = input("Service Name: ")
            username = input("Service Username: ")
            password = input("Service Password: ")
            email = input("Service Email: ")
            
            if self.vault_manager.add_credentials(username, password, email, service):
                print("Credentials added successfully!")
            else:
                print("Failed to add credentials.")
                
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print("An unexpected error occurred.")
            logging.error(f"Error adding credentials: {str(e)}")

    def remove_credentials(self):
        print("\n=== Remove Credentials ===")
        try:
            service = input("Service Name: ")
            username = input("Service Username: ")
            
            if self.vault_manager.delete_credentials(service, username):
                print("Credentials removed successfully!")
            else:
                print("Credentials not found.")
                
        except Exception as e:
            print("An error occurred while removing credentials.")
            logging.error(f"Error removing credentials: {str(e)}")

if __name__ == "__main__":
    try:
        manager = PasswordManager()
        manager.main_menu()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        logging.error(f"Fatal error in main: {str(e)}")

# mkay the tech stack will be
# Cloud - Based Front-end: Vue.js
# Standalone Front-end: Electron.js but i heard it's to bulky fudggeeee
# Back-end: Flask
# Cloud-based Database: Firebase
# Stand-alone Database: SQLite