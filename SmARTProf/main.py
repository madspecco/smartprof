from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Needed for flashing messages


# MySQL Configuration
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="smartprof2"
    )
    return connection


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        connection = create_connection()
        cursor = connection.cursor()

        # Check if the user exists
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()

        # Close the database connection
        cursor.close()
        connection.close()

        if result:
            hashed_password = result[0]

            # Verify the password
            if check_password_hash(hashed_password, password):
                flash("Login successful.", "success")
                return redirect(url_for('select_langauge'))  # Redirect to the select language
            else:
                flash("Invalid username or password.", "error")
        else:
            flash("Invalid username or password.", "error")

    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        # Check username validity
        if len(username) < 5 or len(username) > 10:
            flash("Username must be between 5 and 10 characters long!")
            return redirect(url_for('register'))

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Connect to the database
        connection = create_connection()
        cursor = connection.cursor()

        try:
            # Insert the new user into the users table
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            connection.commit()  # Commit the transaction

            flash("Registration successful! You can now log in.")
            return redirect(url_for('login'))  # Redirect to the login page after registration
        except mysql.connector.Error as err:
            flash(f"Error: {err}")
            return redirect(url_for('register'))
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()

    return render_template('register.html')


@app.route('/select-language')
def select_langauge():
    return render_template('select-language.html')


@app.route('/main-game.html')
def main_game():
    return render_template('main-game.html')


if __name__ == '__main__':
    app.run(debug=True)
