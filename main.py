from user.userHandling import UserHandling
from vault.vaultManager import VaultManager

class PasswordManager:
    def __init__(self):
        self.userHandling = UserHandling()
        self.vaultManager = VaultManager()
        self.loggedIn = False

    def mainMenu(self):
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
            
            if self.userHandling.verifyLogin(username, password):
                self.loggedIn = True
                self.vaultMenu()
                break
            
            attempts -= 1
            print(f"Invalid credentials! {attempts} attempts remaining.")

    def signup(self):
        userData = self.userHandling.createUser()
        if userData:
            # Save user data
            print("Registration successful!")
        else:
            print("Registration cancelled.")

    def vaultMenu(self):
        while self.loggedIn:
            print("\n=== Vault Menu ===")
            print("[D]isplay Vault")
            print("[N]ew Credentials")
            print("[A]rchive Credentials")
            print("[U]nhash Password")
            print("[L]ogout")
            print("[E]xit")
            
            choice = input("Choice: ").lower()
            
            if choice == 'd':
                self.vaultManager.displayVault()
            elif choice == 'n':
                self.addNewCredentials()
            elif choice == 'a':
                self.archiveCredentials()
            elif choice == 'u':
                self.vaultManager.getPassword()
            elif choice == 'l':
                self.loggedIn = False
            elif choice == 'e':
                self.loggedIn = False
                exit()
            else:
                print("Invalid choice!")

    def addNewCredentials(self):
        print("\n=== Add New Credentials ===")
        pass

    def archiveCredentials(self):
        print("\n=== Archive Credentials ===")
        pass

if __name__ == "__main__":
    manager = PasswordManager()
    manager.mainMenu()