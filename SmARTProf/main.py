from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import check_password_hash

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
        # Handle registration logic here
        pass
    return render_template('register.html')


@app.route('/select-language')
def select_langauge():
    return render_template('select-language.html')


@app.route('/main-game.html')
def main_game():
    return render_template('main-game.html')


if __name__ == '__main__':
    app.run(debug=True)
