#CAUTION!  YMMV Only runs on a mac! Uses a utility called sips to resize images and export to differing 
#sizes and qualities. 



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

import subprocess
import sys
import os

def get_image_width(input_path):
    result = subprocess.run(["sips", "-g", "pixelWidth", input_path], capture_output=True, text=True)
    output_lines = result.stdout.strip().split("\n")

    # Extract the numeric value from the output
    try:
        pixel_width = int(output_lines[-1].split(":")[1].strip())
        return pixel_width
    except (ValueError, IndexError):
        print("Error: Unable to extract pixel width.")
        sys.exit(1)

def save_scaled_image(input_path, output_directory, format, scale_percentage, quality=None):
    base_filename, ext = os.path.splitext(os.path.basename(input_path))
    
    if quality:
        output_filename = f"{base_filename}-{format}-SCALE{scale_percentage}-QUALITY{quality}{ext}"
    else:
        output_filename = f"{base_filename}-{format}-SCALE{scale_percentage}{ext}"

    # Ensure the correct file extension for the output file
    output_file_path = os.path.join(output_directory, output_filename)
    output_file_path = output_file_path.replace(ext, f".{format}")

    original_width = get_image_width(input_path)
    new_width = int(original_width * scale_percentage / 100)

    command = [
        "sips",
        "-s", "format", format,
        "--resampleWidth", str(new_width),
        "--out", output_file_path,
        input_path
    ]

    if quality:
        command.extend(["--setProperty", "formatOptions", str(quality)])

    print("About to run:", command)

    subprocess.run(command)

def process_image(input_path, output_directory):
    formats = ["png", "jpeg", "gif", "tga", "bmp"]
    scale_percentages = [90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 2]

    for format in formats:
        for scale_percentage in scale_percentages:
            save_scaled_image(input_path, output_directory, format, scale_percentage)

        if format == "jpeg":
            quality_settings = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 2]
            for quality in quality_settings:
                for scale_percentage in scale_percentages:
                    save_scaled_image(input_path, output_directory, format, scale_percentage, quality)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_image>")
        sys.exit(1)

    input_image = sys.argv[1]
    
    if not os.path.isfile(input_image):
        print("Error: Input file not found.")
        sys.exit(1)

    current_directory = os.getcwd()
    process_image(input_image, current_directory)
