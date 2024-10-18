import base64

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from predict_image import get_predicted_class
from config import PATH_TO_DRAWING, index_dict

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
    language = request.args.get('language')  # Retrieve selected language from query params

    word, context = None, None
    if language:
        print(language)

        # Connect to the database
        connection = create_connection()
        cursor = connection.cursor()

        try:
            # Randomly select a word based on the selected language
            query = f"SELECT {language}, context_{language} FROM words ORDER BY RAND() LIMIT 1;"
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                word = result[0]
                context = result[1]
                session['correct_word'] = word  # Store the correct word in the session
                print(f"Random word: {word}, Context: {context}")  # Print the selected word and its context
            else:
                print("No word found.")
                word, context = None, None  # Handle case where no word is found

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            word, context = None, None  # Handle error case
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()

    # Clear feedback from session after use
    session.pop('feedback', None)

    return render_template('main-game.html', word=word, context=context)


@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({"error": "No image data provided."}), 400

    image_data = data['image']

    # Decode the image data
    header, encoded = image_data.split(',', 1)
    try:
        with open('drawing.png', 'wb') as f:
            f.write(base64.b64decode(encoded))

        predicted_class = int(get_predicted_class(PATH_TO_DRAWING))
        print(f"Predicted class index: {predicted_class}")

        # Get the correct word from the session
        correct_word = session.get('correct_word', "").lower()  # Ensure to convert to lower case for comparison
        print(correct_word)

        if predicted_class in index_dict:
            predicted_words = index_dict[predicted_class]  # Get tuple of words

            # Check if the correct word matches any of the translations
            if correct_word in [word.lower() for word in predicted_words]:
                feedback = "Correct!"
            else:
                feedback = "Incorrect."
        else:
            feedback = "Invalid prediction."

        print(feedback)

        # Store feedback in session and redirect to main game
        return redirect(url_for('main_game'))  # Redirect to main game after processing
    except Exception as e:
        print(f"Prediction error: {str(e)}")  # Log the error
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
