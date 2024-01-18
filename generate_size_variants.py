#Take image and output jpeg variants of it at different sizes (numbers of pixels) from 100-1% 
#Output will be auto named

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
import sys
import os

def scale_image(input_path, output_path, scale_percent):
    with Image.open(input_path) as img:
        width, height = img.size
        new_width = int(width * scale_percent / 100)
        new_height = int(height * scale_percent / 100)
        resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        resized_img.save(output_path)

def generate_scaled_images(input_path):
    file_name, file_ext = os.path.splitext(os.path.basename(input_path))
    
    with Image.open(input_path) as img:
        width, height = img.size

    for scale_percent in range(100, 0, -1):
        scale_str = str(scale_percent).zfill(2)  # Pad with a leading zero if it's a single-digit number
        new_width = int(width * scale_percent / 100)
        new_height = int(height * scale_percent / 100)
        output_path = f"{file_name}_scaled_{scale_str}_{scale_percent}pct_{new_width}x{new_height}.jpeg"
        scale_image(input_path, output_path, scale_percent)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scale_images.py <input_image.jpg>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    
    if not os.path.isfile(input_image_path):
        print(f"Error: '{input_image_path}' is not a valid file.")
        sys.exit(1)

    generate_scaled_images(input_image_path)
    print("Scaled images generated successfully.")

