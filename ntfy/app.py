from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Define the URL of the server
NTFY_SERVER_URL = os.getenv('NTFY_SERVER_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_notification', methods=['POST'])
def send_notification():
    if request.method == 'POST':
        # Get the message from the form input
        message = request.form.get('message')

        if message:
            # Send POST request to the server
            response = requests.post(NTFY_SERVER_URL, data=message.encode(encoding='utf-8'))

            if response.status_code == 200:
                return redirect(url_for('sent'))  # Redirect to the sent page after sending the message
            else:
                return 'Failed to send notification. Please try again.'

        else:
            return 'Please enter a message.'

@app.route('/sent')
def sent():
    return render_template('sent.html')

if __name__ == '__main__':
    app.run(debug=True)

