from PIL import Image
import os

# Input and output directories
input_folder = "Unsorted_Data"
output_folder = "sorted_data"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all images in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        
        # Resize image (removing Image.ANTIALIAS)
        img_resized = img.resize((256, 256))
        
        # Save resized image
        output_path = os.path.join(output_folder, filename)
        img_resized.save(output_path)

print("All images resized successfully!")
