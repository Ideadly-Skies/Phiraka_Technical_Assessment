# imports
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session # type: ignore
from DB import DB
from datetime import datetime  # Import the datetime class
from dotenv import load_dotenv                                                       # type: ignore
import random
import string

"""
===================================
    Load .env + CRUD Functions
===================================
"""
# load dotenv
load_dotenv()

# initialize db class
db = DB()

# login function
def login(username, password):
    return db.login(username, password)

# add new user
def add_user(username, password):
    response = db.insert_user(username, password)
    print("user %s successfully added: %s" %(username, response))

# update user
def update_user(user_id, new_username, new_password):
    response = db.update_user(user_id, new_username, new_password)
    print("User %d updated: %s" %(user_id, response))

# delete user
def delete_user(user_id):
    response = db.delete_user(user_id)
    print("User %d deleted: %s" %(user_id, response))

# get users
def get_users():
    users = db.get_all_users()
    print("printing all users...")
    for user in users:
        print(user)

"""
===================================
      Routes + Flask App Flow
===================================
"""
# init new flask instance
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def index():
    # render login form
    return render_template('login.html')  

# Generate captcha
@app.route('/generate_captcha')
def generate_captcha():
    # Generate random captcha string (5 characters)
    captcha_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    # Store the captcha value in session
    session['captcha'] = captcha_value

    # Return captcha as text or image (depending on your implementation)
    return captcha_value

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    captcha_input = request.form['captcha']

    # get the stored captcha from the session
    stored_captcha = session.get('captcha')

    # match captcha with user input
    print("captcha input: %s" % (captcha_input))
    print("stored captcha: %s" % (stored_captcha))
    
    if captcha_input != stored_captcha: 
        flash("LOGIN GAGAL.", 'error')
        return redirect(url_for('index'))

    if db.login(username, password):
        flash("LOGIN SUKSES", 'success')
        return redirect(url_for('dashboard'))
    else:
        flash("LOGIN GAGAL.", 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # clear entire session
    session.clear()

    # flash successfully logout!
    flash("LOGOUT SUKSES", 'success')

    # Redirect the user to the login page
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Fetch all users from the database
    users = db.get_all_users()

    # Convert CreateTime to datetime and format it
    for user in users:
        # Ensure 'CreateTime' is in datetime format
        if isinstance(user['createtime'], str):
            # Use the correct format for ISO 8601 with microseconds
            user['createtime'] = datetime.strptime(user['createtime'], '%Y-%m-%dT%H:%M:%S.%f')
        # Format the datetime object as 'YYYY-MM-DD'
        user['createtime'] = user['createtime'].strftime('%Y-%m-%d')

    # Render the dashboard template with users data
    return render_template('dashboard.html', users=users)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Add the new user to the database
        db.insert_user(username, password)
        
        flash("BERHASIL MENAMBAHKAN USER BARU!", 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_user.html')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = db.get_user_by_id(user_id)[0]  # Fetch the user by ID
    if request.method == 'POST':
        # If it's a POST request, update the user data
        new_username = request.form['username']
        new_password = request.form['password']
        db.update_user(user_id, new_username, new_password)
        flash("UPDATE BERHASIL!", 'success')
        return redirect(url_for('dashboard'))
    
    # If GET request, render the form with the user's current data
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    db.delete_user(user_id) 
    flash("DELETE BERHASIL!", 'success')
    return redirect(url_for('dashboard'))

"""
===============================
    Invoke Flask App 
===============================
"""
# checks if the current script is being run directly as the main program
# or if it's being imported as a module into another program
if __name__ == "__main__":
    # migrate and create `tbl_user`
    # db.create_table()
    
    app.run(debug=True)