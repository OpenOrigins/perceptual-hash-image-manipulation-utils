#Take image and output jpeg variants of it with quality levels (file size) from 100-1% 
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

def compress_image(input_path, output_path, quality):
    with Image.open(input_path) as img:
        img.save(output_path, 'JPEG', quality=quality)

def generate_output_images(input_path):
    file_name, file_ext = os.path.splitext(os.path.basename(input_path))
    
    for quality in range(100, 0, -1):
        quality_str = str(quality).zfill(2)  # Pad with a leading zero if it's a single-digit number
        output_path = f"{file_name}_quality_{quality_str}.jpeg"
        compress_image(input_path, output_path, quality)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compress_images.py <input_image.jpg>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    
    if not os.path.isfile(input_image_path):
        print(f"Error: '{input_image_path}' is not a valid file.")
        sys.exit(1)

    generate_output_images(input_image_path)
    print("Images generated successfully.")

