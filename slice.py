#Slice image into the number of segments specified
 
"""
Copyright 2023 OpenOrigins 2023

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from PIL import Image
import os
import sys

def slice_image(input_image_path, num_horizontal, num_vertical):
    original_image = Image.open(input_image_path)
    width, height = original_image.size

    # Calculate the size of each slice
    slice_width = width // num_horizontal
    slice_height = height // num_vertical

    # Create output directory
    output_directory = "slices"
    os.makedirs(output_directory, exist_ok=True)

    # Slice the image and save each segment
    for i in range(num_vertical):
        for j in range(num_horizontal):
            left = j * slice_width
            upper = i * slice_height
            right = left + slice_width
            lower = upper + slice_height

            # Crop the image
            slice_image = original_image.crop((left, upper, right, lower))

            # Build the output filename based on location, size, and original filename
            output_filename = f"{output_directory}/slice_{i}_{j}_{slice_width}x{slice_height}_{os.path.basename(input_image_path)}"

            # Save the sliced image
            slice_image.save(output_filename)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python slice.py <input_image_path> <num_horizontal> <num_vertical>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    num_horizontal = int(sys.argv[2])
    num_vertical = int(sys.argv[3])

    slice_image(input_image_path, num_horizontal, num_vertical)
    print(f"Image sliced into {num_horizontal}x{num_vertical} segments.")

