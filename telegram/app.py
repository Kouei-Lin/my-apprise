import os
from dotenv import load_dotenv
from apprise import Apprise

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
INCLUDE_IMAGE = os.getenv('INCLUDE_IMAGE', 'no')  # Default to no if not provided

# Construct notification URL
notification_url = f"tgram://{BOT_TOKEN}/{CHAT_ID}/"
if INCLUDE_IMAGE.lower() == 'yes':
    notification_url += "?image=yes"

# Initialize Apprise object
apobj = Apprise()

# Add notification URL
apobj.add(notification_url)

# Prompt user for input
user_input = input("Enter your message: ")

# Send user input as notification
apobj.notify(
    title='User Input Notification',
    body=user_input
)

print("Notification sent successfully.")

