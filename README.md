# Naitëvarna


**Naitëvarna** is a Python-based encryption tool focused on securing sensitive data using AES encryption. This project leverages the `PyCryptodome` library for cryptographic operations and the `cryptography` package for key derivation using PBKDF2 (Password-Based Key Derivation Function 2). The tool is designed to encrypt and decrypt JSON-based user data securely, with an emphasis on password management applications.


# Installation

- [Windows][null] *No versions available yet for the GUI application.*
- [Linux][null] *No versions available yet for the GUI application.*

Currently, there won't be any versions available for Apple, I hate Apple products with a fury of a thousand suns.
Just kidding! But seriously, [here you go](https://youtu.be/dQw4w9WgXcQ?si=qKYZFide42rUtwAM).


## Requirements

- Python 3.x
- `pycryptodome`
- `cryptography`

Install the dependencies using `pip`:

```bash```
``` pip install pycryptodome cryptography```
In the future, these requirements will be automatically installed via an installer (e.g., .msi or .exe for Windows, and .deb or .rpm for Linux).


### Features

- **AES Encryption with User-Provided Password**: Securely encrypt and decrypt sensitive data using AES encryption.
- **Key Derivation with PBKDF2**: Enhance security by deriving a strong cryptographic key from a user-provided password using PBKDF2.
- **Data Padding and Unpadding**: Ensure compatibility with AES by padding and unpadding data as needed.
- **Save and Load Encrypted Data**: Store encrypted data in files, making it easy to load and decrypt when needed.
- **Password Generation**: Generate secure passwords for websites, offering an option to create a new, stronger password if the current one is deemed insecure.
- **Cloud/Hybrid Service Option**: A premium cloud-hybrid service version available for a fee, providing users with secure, online management of their encrypted data.


# Security

## Password generation
Naitëvarna can generate passwords and you can measure their strength using these:
- [zxcvbn](https://github.com/dropbox/zxcvbn)
- [How Secure Is My Password?](https://howsecureismypassword.net/)
- [Password Meter](https://www.passwordmeter.com/)
- [Have I Been Pwned?](https://haveibeenpwned.com/Passwords)
- [Your Password is Easy](https://yourpasswordiseasy.com) **COMING SOON!!**


# API
Naitëvarna would soon offer a developer API option for integrating the encryption functionality into other applications. You can use the provided functions in your own projects to secure sensitive data.


# Security Considerations
Ensure that the password used for encryption is strong and kept secret.
The salt and IV are randomly generated for each encryption and should be unique for every use.

This tool is intended for local, secure storage and management of sensitive data. It should not be used for cloud-based storage without additional precautions.


# License

The MIT License is chosen because of its simplicity and permissiveness, allowing anyone to freely use, modify, and distribute the code. It supports both open-source and commercial use without requiring the release of source code for derivative works. This approach encourages wide adoption and contribution while providing flexibility for users and developers alike.

# Support Naitëvarna

Naitëvarna is open-source, but we gladly accept donations! If you'd like to support the project, please consider buying us a beer or a pizza:
[PayPal](https://paypal.com)
[Patreon](https://patreon.com)



# Docker

Naitëvarna will soon offer a Docker implementation for easier deployment and management. This will allow you to run Naitëvarna in a containerized environment, ensuring better portability and ease of use across different platforms.

You can customize the ports by modifying the Docker configuration if needed. Please refer to the `docker-compose.yml` file to adjust the configuration according to your specific requirements.


# Code Reviews
If you have any improvements to the code:

Clone the repository
Make your edits
Add your name to the contributors list
Submit a Pull Request (PR) and feel free to inform us about any issues you find

# Contributing
Feel free to fork this repository and submit pull requests. Any improvements, bug fixes, or feature requests are welcome!


