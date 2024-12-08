from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql  # Importing PyMySQL
from flask import session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Establish the MySQL connection using pymysql
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='smart_path_db'  # Use your actual database name here
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

        try:
            with connection.cursor() as cursor:
                # Insert user into the database
                sql = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, email, hashed_password))
                connection.commit()  # Commit the changes to the database
                print(f"Executing query: {sql}")
                print(f"With values: {username}, {email}, {hashed_password}")

            flash("Account created successfully! Please log in.")
            
            # Log the user in automatically after signup
            session['user_email'] = email
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('signup'))

    # Render the signup page if GET request
    return render_template('login_signup_page.html', page='signup')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with connection.cursor() as cursor:
                # Fetch user data from the database
                sql = "SELECT password_hash FROM Users WHERE email = %s"
                cursor.execute(sql, (email,))
                result = cursor.fetchone()

                if result and check_password_hash(result[0], password):
                    session['user_email'] = email  # Set session data
                    flash("Login successful!")
                    return redirect(url_for('index'))  # Redirect to the index page after successful login
                else:
                    flash("Invalid email or password.")
                    return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('login'))

    # Render the login page if GET request
    return render_template('login_signup_page.html', page='login')

@app.route('/')
def index():
    if 'user_email' in session:
        # Render the index.html page when the user is logged in
        return render_template('index.html')  # Serve index page template
    else:
        flash("Please log in to view the homepage.")
        return redirect(url_for('login'))  # Redirect to login if not logged in

@app.route('/logout')
def logout():
    session.pop('user_email', None)  # Remove user_email from session to log out
    flash("You have been logged out.")
    return redirect(url_for('login'))  # Redirect to login after logout

@app.route('/about')
def about():
    return render_template('about.html')  # Serve your about page template

@app.route('/dashboard')
def dashboard():
    if 'user_email' in session:
        return render_template('dashboard.html')  # Render the dashboard page
    else:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('login'))  # Redirect to login if not logged in

if __name__ == '__main__':
    app.run(debug=True)