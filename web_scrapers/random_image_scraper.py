#!/usr/bin/env python3
import os
import requests
import time
import sys


# Determine where this shoddy script is hanging out
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "random_images")
os.makedirs(output_dir, exist_ok=True)

# Print out the download directory 
print("Download directory: " + output_dir)

# Basic config: number of images & the URL for our crappy 256x256 pics
num_images = 10
base_url = "https://picsum.photos/256/256"

# Some ASCII spinner for pre-download animation (just for kicks)
spinner = ['|', '/', '-', '\\']
print("\nHold up, setting shit up...")
for i in range(8):
    sys.stdout.write("\rGetting ready " + spinner[i % len(spinner)])
    sys.stdout.flush()
    time.sleep(0.1)
print("\nLet's fucking go!\n")

# Progress bar settings
bar_length = 30  # length of the progress bar

# Start downloading images 
for i in range(1, num_images + 1):
    # Construct the filename
    filename = os.path.join(output_dir, f"image_{i:04d}.jpg")
    try:
        # Try to get the damn image from the web
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()  # No HTTP bullshit allowed!
        with open(filename, "wb") as f:
            f.write(response.content)
        # Chill for a moment to not hammer the server
        time.sleep(0.2)
    except Exception as e:
        # If shit hits the fan, complain and move on
        error_message = f"Error downloading {filename}: {e}. Fuck it, moving on!"
        sys.stdout.write("\n" + error_message + "\n")
    
    # Calculate progress
    progress = i / num_images
    percent = int(progress * 100)
    filled_length = int(bar_length * progress)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    
    # Only show current file's name with progress info updating in real time
    progress_info = f"Downloading: {os.path.basename(filename)} |{bar}| {percent}% ({i}/{num_images})"
    sys.stdout.write("\r" + progress_info)
    sys.stdout.flush()

print("\n\nAll done :)\n")
