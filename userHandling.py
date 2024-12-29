from cryptography.fernet import Fernet
import base64
import random
import json
import os


    # check if the password is strong enough
def passwordCheck(password):
    # check if the password is at least 8 characters long
    if len(password) < 8:
        return False
    # check if the password contains at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False
    # check if the password contains at least one lowercase letter
    if not any(char.islower() for char in password):
        return False
    # check if the password contains at least one digit
    if not any(char.isdigit() for char in password):
        return False
    # check if the password contains at least one special character
    if not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?/~`' for char in password):
        return False
    # if all the checks pass, return True
    return True

def createUser():
    # create a user
    # get the user email
    userEmail = input('Enter your email: ')
    # get the user name
    userName = input('Enter your name: ')


# Constructing a simple Login
import json
from tabulate import tabulate


def mainMenu():
    print("\n\t\tMain Menu\n")
    choice = input("[S]ignup \n[L]ogin \n[E]xit\nInput: ")
    if (choice == "L" or choice == "l"):
        login()
    elif (choice == "S" or choice == "s"):
        signup()
    elif (choice == "E" or choice == "e"):
        print("...Exiting")
        exit()
    else:
        print("\n\t# Error. Invalid Choice")
        mainMenu()


def login():
    print("\n\t\tLogin Form\n")
    counter = 3
    loggedIn = False
    while (counter > 0) and (loggedIn == False):
        credentialUsr = input("Username: ")
        credentialPsw = input("Password: ")        
        username = "admin"
        password = "admin"

        if (credentialUsr == username) and (credentialPsw == password):
            print("# Login Succesful.")
            loggedIn = True
            menu()
        else:
            counter -= 1
            if (counter > 0):
                print("\n\t# Incorrect Username or Password. Try Again.")
            else:
                print("\n\tYou've exceeded the number of tries. Try again later.")

def signup():
    print("Signup Template")


def menu():

    print("\n\t\tUser Dashboard\n")
    options = input("\n[D]isplay Vault \n[N]ew Credentials \n[A]rchive Credentials\n[L]ogout\n[E]xit\nEnter Option: ")
    if (options == "D") or (options == "d"):
        displayVault()
    elif (options == "N") or (options == "n"):
        newCreds()
    elif (options == "A") or (options == "a"):
        arcCreds()
    elif (options == "L") or (options == "l"):
        loggedIn = False
        mainMenu()
    elif (options == "E") or (options == "e"):
        print("...Exiting Program")
        exit()
    else:
        print("Incorrect Option")
        menu()


def displayVault():
    with open('data.json', 'r') as file:
        data = json.load(file)
    
    headers = ["Username", "Password", "Email", "Website"]
    rows = [[d["username"], d["password"], d["email"], d["website"]] for d in data]
    
    # Print data as a table
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    menu()

def newCreds():
    print("New Creds template")
    menu()

def arcCreds():
    print("Archive Credentials template")
    menu()


mainMenu()