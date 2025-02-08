#!/usr/bin/env python3
import os
import requests
import time
import sys

# *************************************************
# Yo, legend coder!
# This script uses the Openverse API to snag at least 1026 leaf images
# for your ML project. We're searching for "leaves" and paging through results.
# If something breaks, well... fuck it, we just skip that one!
# *************************************************

# Determine the script's crib and create the output folder
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "leaf_images")
os.makedirs(output_dir, exist_ok=True)
print("Download directory: " + output_dir)

# Config: target number of images & Openverse API details
num_images = 1026
downloaded = 0
page = 1
page_size = 100  # how many images per API page
base_search_url = "https://api.openverse.engineering/v1/images/"

# Spinner animation to get you hyped before we start downloading
spinner = ['|', '/', '-', '\\']
print("\nWarming up the engine...")
for i in range(8):
    sys.stdout.write("\rSpinning: " + spinner[i % len(spinner)])
    sys.stdout.flush()
    time.sleep(0.1)
print("\nLet's get these damn leaves!\n")

# Progress bar settings
bar_length = 30

while downloaded < num_images:
    params = {
        "q": "leaves",
        "page": page,
        "page_size": page_size
        # You can add more params here (e.g., license_type) if needed.
    }
    try:
        resp = requests.get(base_search_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            print("\nNo more images found, stopping here.")
            break
    except Exception as e:
        print(f"\nError fetching image data on page {page}: {e}. Skipping this page...")
        page += 1
        continue

    for item in results:
        if downloaded >= num_images:
            break
        image_url = item.get("url")
        if not image_url:
            continue

        current_file = f"leaf_{downloaded+1:04d}.jpg"
        filename = os.path.join(output_dir, current_file)
        try:
            img_resp = requests.get(image_url, timeout=10)
            img_resp.raise_for_status()
            with open(filename, "wb") as f:
                f.write(img_resp.content)
            # Sleep a bit to avoid hammering the server – we ain't machines!
            time.sleep(0.2)
        except Exception as e:
            sys.stdout.write(f"\nError downloading {current_file}: {e}. Skipping this one!")
            continue

        downloaded += 1
        # Update our noob-style ASCII progress bar
        progress = downloaded / num_images
        percent = int(progress * 100)
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        progress_info = f"Downloading: {current_file} |{bar}| {percent}% ({downloaded}/{num_images})"
        sys.stdout.write("\r" + progress_info)
        sys.stdout.flush()

    page += 1

print("\n\nAll done! Collected leaf images for your ML project. Now go kick some ass with that binary filter!\n")
