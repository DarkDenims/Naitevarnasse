
# Naitëvarna

**Naitëvarna** is a Python-based encryption tool focused on securing sensitive data using AES encryption. This project leverages the `PyCryptodome` library for cryptographic operations and the `cryptography` package for key derivation using PBKDF2 (Password-Based Key Derivation Function 2). The tool is designed to encrypt and decrypt JSON-based user data securely, with an emphasis on password management applications.

## Requirements

- Python 3.x
- `pycryptodome`
- `cryptography`

Install the dependencies using `pip`:

```bash```
``` pip install pycryptodome cryptography```

# Features
 - AES encryption with a user-provided password.
 - Key derivation using PBKDF2 for better security.
 - Padding and unpadding of data for compatibility with AES.
 - Save and load encrypted data to/from files.
 - Example implementation for encrypting and decrypting password manager entries.

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
This project is licensed under the MIT License.

# Support Naitëvarna
Naitëvarna is open-source, but we gladly accept donations! If you'd like to support the project, please consider buying us a beer or a pizza:
PayPal
Patreon

# Code Reviews
If you have any improvements to the code:

Clone the repository
Make your edits
Add your name to the contributors list
Submit a Pull Request (PR) and feel free to inform us about any issues you find


# Docker
To run Naitëvarna in a Docker container:

Build the Docker image:
```bash```
Copy code
```docker build -t naitvevarna .```
Run the container:
```bash```
Copy code
```docker run -p 8080:8080 naitvevarna```
The application will be accessible via port 8080.
You can customize the ports by modifying the Docker configuration if needed.

# Contributing
Feel free to fork this repository and submit pull requests. Any improvements, bug fixes, or feature requests are welcome!


# Naitëvarna

**Naitëvarna** is a Python-based encryption tool focused on securing sensitive data using AES encryption. This project leverages the `PyCryptodome` library for cryptographic operations and the `cryptography` package for key derivation using PBKDF2 (Password-Based Key Derivation Function 2). The tool is designed to encrypt and decrypt JSON-based user data securely, with an emphasis on password management applications.

## Requirements

- Python 3.x
- `pycryptodome`
- `cryptography`

Install the dependencies using `pip`:

```bash```
``` pip install pycryptodome cryptography```

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
This project is licensed under the MIT License.

# Support Naitëvarna
Naitëvarna is open-source, but we gladly accept donations! If you'd like to support the project, please consider buying us a beer or a pizza:
PayPal
Patreon

# Code Reviews
If you have any improvements to the code:

Clone the repository
Make your edits
Add your name to the contributors list
Submit a Pull Request (PR) and feel free to inform us about any issues you find


# Docker
To run Naitëvarna in a Docker container:

Build the Docker image:
```bash```
Copy code
```docker build -t naitvevarna .```
Run the container:
```bash```
Copy code
```docker run -p 8080:8080 naitvevarna```
The application will be accessible via port 8080.
You can customize the ports by modifying the Docker configuration if needed.

# Contributing
Feel free to fork this repository and submit pull requests. Any improvements, bug fixes, or feature requests are welcome!

