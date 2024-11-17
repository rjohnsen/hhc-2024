import os
from PIL import Image
import numpy as np
import glob

# Set the directory containing the shredded images
image_dir = "/mnt/c/Users/Roger Johnsen/Downloads/HHC2024/shreds/slices"

# Set the number of rows and columns in the final stitched image
rows = 20
cols = 50

# Use glob to find all image files in the directory
image_files = glob.glob(os.path.join(image_dir, '*.jpg'))  # Match all .jpg files that fit the naming pattern

print(image_files)

# Sort the files (assuming they're numbered sequentially like piece_0000.jpg, piece_0001.jpg, ...)
image_files.sort()

# Load all the image pieces
image_pieces = [Image.open(img_file) for img_file in image_files]

# Get the size of an individual image piece (assuming all pieces are the same size)
piece_width, piece_height = image_pieces[0].size

# Create an empty image with a size that can hold all the pieces
stitched_image = Image.new('RGB', (piece_width * cols, piece_height * rows))

# Paste each piece into the correct location in the stitched image
for i in range(rows):
    for j in range(cols):
        # Calculate the position of the current piece in the final image
        x_offset = j * piece_width
        y_offset = i * piece_height
        
        # Paste the current piece into the stitched image
        stitched_image.paste(image_pieces[i * cols + j], (x_offset, y_offset))

# Save the stitched image
stitched_image.save("/mnt/c/Users/Roger Johnsen/Downloads/HHC2024/stitched_image.jpg")

# Optionally show the stitched image
stitched_image.show()