from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

# Function to initialize MySQL configuration
def init_app(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'  # Your MySQL username
    app.config['MYSQL_PASSWORD'] = 'password'  # Your MySQL password
    app.config['MYSQL_DB'] = 'mysql'  # Use the 'mysql' database as the default one to connect to
    mysql.init_app(app)

# Function to test the database connection and setup
def test_connection(app):
    try:
        # Use mysql.connection to get a connection
        connection = mysql.connection
        cursor = connection.cursor()

        # Create database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS smart_path_db;")
        connection.commit()  # Commit the creation of the database

        # Now switch to the created database
        cursor.execute("USE smart_path_db;")  

        # Create Users table if it does not exist
        create_users_table_query = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_users_table_query)
        connection.commit()  # Commit the creation of the Users table

        # Create metacognitionresults table if it does not exist (updated with session_id)
        create_metacognitionresults_table_query = """
        CREATE TABLE IF NOT EXISTS metacognitionresults (
            session_id VARCHAR(40) NOT NULL,  -- Using session_id instead of assessment_id
            user_email VARCHAR(255) NOT NULL,
            results TEXT NOT NULL,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Set current timestamp by default
            PRIMARY KEY (session_id, user_email),  -- Primary key ensures uniqueness per user per session
            FOREIGN KEY (user_email) REFERENCES Users(email) ON DELETE CASCADE
        );
        """
        cursor.execute(create_metacognitionresults_table_query)
        connection.commit()  # Commit the creation of the metacognitionresults table

        # Create assessmentresults table if it does not exist
        create_assessmentresults_table_query = """
        CREATE TABLE IF NOT EXISTS assessmentresults (
            session_id VARCHAR(40) NOT NULL,  -- Using session_id as the assessment identifier
            user_id INT NOT NULL,
            assessment_type VARCHAR(255) NOT NULL,
            results TEXT NOT NULL,
            PRIMARY KEY (session_id, user_id),  -- Primary key ensures uniqueness per user per session
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
        );
        """
        cursor.execute(create_assessmentresults_table_query)
        connection.commit()  # Commit the creation of the assessmentresults table

        # Verify that we are connected to the database
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        print("Connected to database:", db)

        cursor.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")

# Example of initializing and testing the connection
app = Flask(__name__)
init_app(app)

with app.app_context():
    test_connection(app)