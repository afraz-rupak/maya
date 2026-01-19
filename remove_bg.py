"""
Script to remove background from logo image
"""
from PIL import Image
from rembg import remove
import os

# Input and output paths
input_path = "/Volumes/afraz_SSD/maya/maya_logo.png"
output_path = "/Volumes/afraz_SSD/maya/frontend/assets/maya_logo.png"

# Check if input file exists
if not os.path.exists(input_path):
    print(f"Error: Input file not found at {input_path}")
    print("Please save the logo as 'image.png' in the project root directory")
    exit(1)

# Open the image
with open(input_path, 'rb') as i:
    input_image = i.read()

# Remove background
output_image = remove(input_image)

# Save the result
with open(output_path, 'wb') as o:
    o.write(output_image)

print(f"✓ Background removed successfully!")
print(f"✓ Logo saved to: {output_path}")
