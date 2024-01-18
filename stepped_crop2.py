#Generate a number of cropped images of a specified size, then use the granularity as a pixel boundary to be able
#to be find that number of images of this size int he original.  Then step down... 

#python ../stepped_crop2.py ./hawker_fury.jpeg . 64 3
#Generated 1 cropped images for 4032x3024 in ..
#Generated 374 cropped images for 3968x2976 in ..
#Generated 1419 cropped images for 3904x2928 in ..
#Generated 3185 cropped images for 3840x2880 in ..
#...

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

def crop_to_aspect_ratio(image, x, y, target_width, target_height, aspect_ratio):
    return image.crop((x, y, x + target_width, y + target_height))

def generate_cropped_images(input_image_path, output_directory, width, height, x_step=16, y_step=9):
    original_image = Image.open(input_image_path)
    original_width, original_height = original_image.size

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    count = 0
    x = 0
    while x + width <= original_width:
        y = 0
        while y + height <= original_height:
            # Crop the image to the desired aspect ratio
            cropped_image = crop_to_aspect_ratio(original_image, x, y, width, height, aspect_ratio)

            # Save the cropped image
            output_filename = f"cropped_{os.path.basename(input_image_path)}_{width}x{height}_x{x}_y{y}.jpg"
            output_path = os.path.join(output_directory, output_filename)
            cropped_image.save(output_path)

            count += 1
            y += y_step

        x += x_step

    print(f"Generated {count} cropped images for {width}x{height} in {output_directory}.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python generate_cropped_images.py <input_image_path> <output_directory> <step> <granularity>")
        print("step is the size to reduce the image by for each iteration (min 1), granularity is how many pixels wiggle we use to fit inside the original min 1. Minimums for both will yield larger numebrs of files")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_directory = sys.argv[2]
    granularity = int(sys.argv[4]) #this is the amount of wiggle that we can use inside the image - min 1 will generate most cropped images
    step = int(sys.argv[3])

    original_image = Image.open(input_image_path)
    original_width, original_height = original_image.size

    aspect_ratio = original_width/original_height

    width = original_width
    while width > 0:
        height = int(width / aspect_ratio)

        generate_cropped_images(input_image_path, output_directory, width, height, granularity, granularity)

        width -= step

    print("Script completed.")
