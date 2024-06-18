# SecureAuth-Flask-App

## Description

This is a simple Flask web application for user registration and login with data encryption.

## Key Features

### User Registration

- Users can fill out a form with username, password, and email address.
- User data is encrypted using the `cryptography.fernet` library.
- Encrypted data is stored in the `UserReg.txt` file. Each user entry is separated by a line of 50 dashes (-).

### User Login

- Users can log in by entering their username and password.
- User data is read from the `UserReg.txt` file, decrypted, and checked against the entered credentials.
- Upon successful login, users are redirected to a search page (a simple HTML page resembling Google).

### Error Handling

- Errors are logged in the `Errors.txt` file in case of exceptions during registration or login.
- Relevant error messages are displayed on the application's web pages.

## Technical Details

- **Technologies Used:** Python, Flask, `cryptography.fernet` for data encryption.
- The web interface is presented through HTML templates handled by Flask route functions.
- The project includes basic logic for user management without using a database, making it simple to set up and use.

This code can be useful for creating a basic authentication and registration system for small web applications or prototypes that do not require complex database infrastructure.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TDimash/SecureAuth-Flask-App.git
   cd SecureAuth-Flask-App
