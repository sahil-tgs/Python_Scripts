#!/usr/bin/env python3
import os
import shutil
import random
import sys

# List your source folders here – change these to your actual folder paths
source_folders = ["Leaf_Spot", "Healthy", "Sterilic_mosaic", "Leaf_webber", "sorted_data"]

# Destination folder where merged images will be copied
merged_folder = "Leaves"

# Create the merged folder if it doesn't already exist
if not os.path.exists(merged_folder):
    os.makedirs(merged_folder)

# Allowed image extensions (case insensitive)
allowed_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}

print("Starting to merge and rename images...\n")

# Count total images from all folders
total_images = 0
for folder in source_folders:
    for filename in os.listdir(folder):
        ext = os.path.splitext(filename)[1].lower()
        if ext in allowed_extensions:
            total_images += 1

# Function to print a Unicode progress bar
def print_progress_bar(current, total, bar_length=30):
    progress = current / total
    filled_length = int(bar_length * progress)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    percent = int(progress * 100)
    sys.stdout.write(f"\rProcessing: |{bar}| {percent}% ({current}/{total})")
    sys.stdout.flush()

processed_images = 0
# Keep track of used filenames to avoid collisions
used_names = set()

# Loop through each source folder
for folder in source_folders:
    for filename in os.listdir(folder):
        ext = os.path.splitext(filename)[1].lower()
        if ext in allowed_extensions:
            # Generate a random number for the filename and ensure uniqueness
            rand_num = random.randint(100000, 999999)
            new_name = f"image-{rand_num}{ext}"
            while new_name in used_names:
                rand_num = random.randint(100000, 999999)
                new_name = f"image-{rand_num}{ext}"
            used_names.add(new_name)

            src_path = os.path.join(folder, filename)
            dst_path = os.path.join(merged_folder, new_name)
            
            shutil.copy2(src_path, dst_path)
            processed_images += 1
            print_progress_bar(processed_images, total_images)

print("\n\nAll done, your merged folder is ready!")
