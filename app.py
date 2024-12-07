from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

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

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirmPassword']

    # Validate passwords
    if password != confirm_password:
        flash("Passwords do not match!")
        return redirect(url_for('login_page'))

    # Hash the password
    hashed_password = generate_password_hash(password)

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Insert user into the database
            sql = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, email, hashed_password))
            connection.commit()
        flash("Account created successfully! Please log in.")
        return redirect(url_for('login_page'))
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('login_page'))
    finally:
        connection.close()

# Login Route
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Fetch user data from the database
            sql = "SELECT password_hash FROM Users WHERE email = %s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
            
            if result and check_password_hash(result[0], password):
                flash("Login successful!")
                return redirect(url_for('dashboard'))  # Replace with your dashboard route
            else:
                flash("Invalid email or password.")
                return redirect(url_for('login_page'))
    except Exception as e:
        flash(f"An error occurred: {e}")
        return redirect(url_for('login_page'))
    finally:
        connection.close()

# Render Login and Signup Page
@app.route('/')
@app.route('/login-page')
def login_page():
    return render_template('login.html')  # Your login and signup HTML

# Dashboard (Dummy Route)
@app.route('/dashboard')
def dashboard():
    return "Welcome to the Dashboard!"  # Replace with your actual dashboard page

if __name__ == '__main__':
    app.run(debug=True)