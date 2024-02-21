import os
import psutil
from apprise import Apprise
from dotenv import load_dotenv
from time import sleep

# Load environment variables from .env file
load_dotenv()

def get_line_url():
    """Constructs the Line URL from environment variables."""
    line_token = os.getenv('LINE_TOKEN')
    line_user = os.getenv('LINE_USER')
    if line_token is None or line_user is None:
        print("Error: LINE_TOKEN or LINE_USER not found in .env file.")
        return None
    return f'line://{line_token}/{line_user}'

def send_notification(message, line_url):
    """Sends a notification using Line Notify."""
    if line_url is None:
        return
    apobj = Apprise()
    apobj.add(line_url)
    apobj.notify(body=message)

def monitor_disk_usage(interval=10):
    """Monitors disk usage and sends notifications every specified interval."""
    line_url = get_line_url()
    while True:
        # Get disk partitions
        disk_partitions = psutil.disk_partitions(all=True)
        # Initialize variables to accumulate disk usage information
        disk_info = []

        # Iterate through all disk partitions
        for partition in disk_partitions:
            disk_name = partition.device
            # Check if disk is of interest (/dev/sd*)
            if disk_name.startswith('/dev/sd'):
                # Get disk usage for each partition
                disk_usage = psutil.disk_usage(partition.mountpoint)
                # Calculate disk usage percentage
                disk_usage_percent = disk_usage.percent
                # Get the total disk size
                total_disk_size = disk_usage.total / (2**30)  # Convert to GB
                # Get the amount of disk space used
                used_disk_space = disk_usage.used / (2**30)  # Convert to GB
                # Append disk information to the list
                disk_info.append(f"Disk {disk_name} usage: {disk_usage_percent}%, Total: {total_disk_size:.2f} GB, Used: {used_disk_space:.2f} GB")

        # Prepare notification message with all disk information
        message = "\n".join(disk_info)

        # Send notification if there's disk information to send
        if disk_info:
            send_notification(message, line_url)

        # Wait for specified interval before sending the next notification
        sleep(interval)

if __name__ == "__main__":
    # Set the interval for sending notifications (in seconds)
    interval = 10
    monitor_disk_usage(interval)

