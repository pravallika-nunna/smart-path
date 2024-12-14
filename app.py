from datetime import timedelta
from flask import Flask, json, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask import session
import os
import uuid

# Initialize Flask app
 # Generates a secure random secret key
app = Flask(__name__)

# Configure session timeout (if desired)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session timeout to 30 minutes
app.secret_key = str(uuid.uuid4())  # Use a cryptographically secure random secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Use Secure cookies (only for HTTPS)
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent access to the cookie from JavaScript

# Establish MySQL connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='smart_path_db'
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
                connection.commit()

            flash("Account created successfully! Please log in.")
            
            # Log the user in automatically after signup
            session['user_email'] = email
            session.permanent = True  # Make the session permanent so it expires after the configured time
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred: {e}")
            return redirect(url_for('signup'))

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
    is_logged_in = 'user_email' in session
    return render_template('index.html', is_logged_in=is_logged_in)

@app.route('/forms')
def forms():
    session.pop('quiz_results', None)
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
    session.clear()
    session.pop('user_email', None)  # Remove user_email from session to log out
    flash("You have been logged out.")
    return redirect(url_for('index'))  # Redirect to login after logout

@app.route('/submit-results', methods=['POST'])
def submit_results():
    # Retrieve JSON data from the request
    quiz_results = request.get_json()

    if 'user_email' not in session:
        return jsonify({"error": "User not logged in"}), 401

    user_email = session['user_email']
    session_id = app.secret_key  # Use the app's secret_key as the session_id

    # Check if the quiz_results is a list (which it should be)
    if isinstance(quiz_results, list):
        try:
            with connection.cursor() as cursor:
                # Insert results into the database using parameterized queries
                sql = """INSERT INTO MetacognitionResults (user_email, results, session_id)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE results = VALUES(results), submitted_at = CURRENT_TIMESTAMP"""

                # Pass parameters directly, pymysql will handle escaping
                cursor.execute(sql, (user_email, json.dumps(quiz_results), session_id))
                connection.commit()
                print("Results stored successfully for user:", user_email)
        except Exception as e:
            print("Error storing results:", e)
            return jsonify({"error": "An error occurred while storing results"}), 500

        return jsonify({"message": "Results submitted successfully"}), 200

    else:
        return jsonify({"error": "Invalid data format. Expected a list."}), 400

from flask import render_template, session, flash, redirect, url_for
import json
import pymysql  # Assuming you're using MySQL for connection

@app.route('/results')
def results():
    if 'user_email' not in session:
        flash("Please log in to view your results.")
        return redirect(url_for('login'))

    user_email = session['user_email']

    try:
        with connection.cursor() as cursor:
            # Retrieve the most recent results from MetacognitionResults for the logged-in user
            sql = """
               SELECT session_id, results, assessment_type
                FROM MetacognitionResults
                WHERE user_email = %s
                ORDER BY session_id DESC LIMIT 1;
            """

            cursor.execute(sql, (user_email,))
            result = cursor.fetchone()

            if not result:
                flash("No results found for your account.")
                return redirect(url_for('forms'))

            session_id, quiz_results, assessment_type = result
            quiz_results = json.loads(quiz_results)  # Parse the JSON string
            print("Fetched Results:", quiz_results)  # Debugging log
    except Exception as e:
        print("Error fetching results:", e)
        flash("An error occurred while fetching your results.")
        return redirect(url_for('forms'))

    return render_template('results.html', quiz_results=quiz_results)  # Ensure you pass `quiz_results`

@app.route('/questions.json')
def serve_questions():
    with open('questions.json') as f:
        data = f.read()
    return data

if __name__ == '__main__':
    app.run(debug=True)