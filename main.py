from flask import Flask, request, render_template_string, redirect, url_for
from cryptography.fernet import Fernet
import logging

app = Flask(__name__)

logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

key = Fernet.generate_key()
cipher_suite = Fernet(key)

registration_form = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Registration</title>
  </head>
  <body>
    <div>
      <h2>Registration Form</h2>
      <form method="POST" action="/register">
        <label for="username">User Name:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br>
        <label for="email">Email:</label><br>
        <input type="email" id="email" name="email"><br><br>
        <input type="submit" value="Register">
      </form>
      <br>
      <a href="/login">Login</a>
    </div>
  </body>
</html>
'''

login_form = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Login</title>
  </head>
  <body>
    <div>
      <h2>Login Form</h2>
      <form method="POST" action="/login">
        <label for="username">User Name:</label><br>
        <input type="text" id="username" name="username"><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password"><br><br>
        <input type="submit" value="Login">
      </form>
      <br>
      <a href="/">Register</a>
    </div>
  </body>
</html>
'''

post_registration_page = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Search</title>
    <style>
      body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
      .logo { font-size: 64px; color: #4285F4; }
      .search-box { margin-top: 40px; }
      .search-box input[type="text"] { width: 50%; padding: 10px; font-size: 18px; }
      .search-box input[type="submit"] { padding: 10px 20px; font-size: 18px; }
    </style>
  </head>
  <body>
    <div class="logo">Google</div>
    <div class="search-box">
      <form method="GET" action="https://www.google.com/search">
        <input type="text" name="q" placeholder="Search Google">
        <input type="submit" value="Search">
      </form>
    </div>
  </body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(registration_form)

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        encrypted_username = cipher_suite.encrypt(username.encode()).decode()
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        encrypted_email = cipher_suite.encrypt(email.encode()).decode()
        
        with open('UserReg.txt', 'a') as f:
            f.write(f'User Name: {encrypted_username}\n')
            f.write(f'Password: {encrypted_password}\n')
            f.write(f'Email: {encrypted_email}\n')
            f.write(f'{"-"*50}\n')
        
        logging.info('User registered')
        
        return redirect(url_for('search_page'))
    except Exception as e:
        with open('Errors.txt', 'a') as error_file:
            error_file.write(f"Registration error: {e}\n")
        return 'An error occurred during registration. Please try again later.', 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            with open('UserReg.txt', 'r') as f:
                lines = f.readlines()
                users = []
                user = {}
                for line in lines:
                    if line.strip() == '-'*50:
                        users.append(user)
                        user = {}
                    else:
                        key, value = line.split(': ')
                        user[key.strip()] = value.strip()
            
            for user in users:
                decrypted_username = cipher_suite.decrypt(user['User Name'].encode()).decode()
                decrypted_password = cipher_suite.decrypt(user['Password'].encode()).decode()
                
                if username == decrypted_username and password == decrypted_password:
                    logging.info('User logged in')
                    return redirect(url_for('search_page'))
            
            return 'Invalid credentials. Please try again.'
        except Exception as e:
            with open('Errors.txt', 'a') as error_file:
                error_file.write(f"Login error: {e}\n")
            return 'An error occurred during login. Please try again later.', 500
    
    return render_template_string(login_form)

@app.route('/search')
def search_page():
    return render_template_string(post_registration_page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
