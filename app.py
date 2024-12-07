from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask import session
from db import test_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='your_password',
        db='your_database'
    )

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Validate passwords
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        connection = None  # Initialize the connection variable

        try:
            connection = get_db_connection()  # Open connection
            with connection.cursor() as cursor:
                # Insert user into the database
                sql = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, email, hashed_password))
                connection.commit()
            flash("Account created successfully! Please log in.")
            
            # Log the user in automatically after signup
            session['user_email'] = email
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('signup'))
        finally:
            if connection:  # Only close connection if it was successfully created
                connection.close()

    # Render the signup page if GET request
    return render_template('login_signup_page.html', page='signup')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = None  # Initialize the connection variable

        try:
            connection = get_db_connection()  # Open connection
            with connection.cursor() as cursor:
                # Fetch user data from the database
                sql = "SELECT password_hash FROM Users WHERE email = %s"
                cursor.execute(sql, (email,))
                result = cursor.fetchone()

                if result and check_password_hash(result[0], password):
                    session['user_email'] = email  # Set session data
                    flash("Login successful!")
                    return redirect(url_for('dashboard'))
                else:
                    flash("Invalid email or password.")
                    return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('login'))
        finally:
            if connection:  # Only close connection if it was successfully created
                connection.close()

    # Render the login page if GET request
    return render_template('login_signup_page.html', page='login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')  # Serve your about page template

    
@app.route('/dashboard')
def dashboard():
    if 'user_email' in session:
        return f"Welcome {session['user_email']} to the Dashboard!"
    else:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)