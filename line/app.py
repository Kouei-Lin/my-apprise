from flask import Flask, render_template, request, redirect, url_for
from apprise import Apprise
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Apprise
apobj = Apprise()

# Read Line token and user from environment variables
line_token = os.getenv('LINE_TOKEN')
line_user = os.getenv('LINE_USER')
line_url = f'line://{line_token}/{line_user}'

# Add Line URL to Apprise
apobj.add(line_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    # Get the message from the form input
    message = request.form.get('message')

    # Send message using Apprise when button is pressed
    if message:
        apobj.notify(
            title='New Message',
            body=message
        )
        return redirect(url_for('sent'))  # Redirect to the sent page after sending the message
    else:
        return 'Please enter a message.'

@app.route('/sent')
def sent():
    return render_template('sent.html')

if __name__ == '__main__':
    app.run(debug=True)

