from datetime import timedelta
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql  # Importing PyMySQL
from flask import session
import os

# Generates a secure random secret key
app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session timeout
#app.secret_key = 'your_secret_key'  # Ensure the secret key is set for session handling
app.secret_key = os.urandom(24) 

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with connection.cursor() as cursor:
                sql = "SELECT password_hash FROM Users WHERE email = %s"
                cursor.execute(sql, (email,))
                result = cursor.fetchone()

                if result and check_password_hash(result[0], password):
                    session['user_email'] = email
                    session.permanent = True  # Ensure the session is permanent
                    flash("Login successful!")
                    return redirect(url_for('index'))  # Redirect after successful login
                else:
                    flash("Invalid email or password.")
                    return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('login'))

    return render_template('login_signup_page.html', page='login')


@app.route('/')
def index():
    # Check if the user is logged in
    is_logged_in = 'user_email' in session
    return render_template('index.html', is_logged_in=is_logged_in)


@app.route('/forms')
def forms():
    print("Session:", session)
    # Check if the user is logged in
    if 'user_email' in session:
        return render_template('forms.html', page="forms", is_logged_in=True)
    else:
        flash("Please log in to attempt the quiz.")
        return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_email' in session:
        return render_template('dashboard.html', is_logged_in=True)
    else:
        flash("Please log in to access the dashboard.")
        return redirect(url_for('login'))


@app.route('/about')
def about():
    # Pass login status to the about page
    is_logged_in = 'user_email' in session
    return render_template('about.html', is_logged_in=is_logged_in)

@app.route('/logout')
def logout():
    session.pop('user_email', None)  # Remove user_email from session to log out
    flash("You have been logged out.")
    return redirect(url_for('index'))  # Redirect to login after logout

@app.route('/submit-results', methods=['POST'])
def submit_results():
    global quiz_results
    quiz_results = request.get_json()  # Retrieve JSON data from the request
    print("Received Results:", quiz_results)  # Debugging log
    return '', 200  # Return an HTTP 200 status

@app.route('/results')
def results():
    global quiz_results
    if not quiz_results:
        return "No results to display", 400  # Handle cases with no results
    return render_template('results.html', results=quiz_results)

@app.route('/questions.json')
def serve_questions():
    with open('questions.json') as f:
        data = f.read()
    return data



if __name__ == '__main__':
    app.run(debug=True)