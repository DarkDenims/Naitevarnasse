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
