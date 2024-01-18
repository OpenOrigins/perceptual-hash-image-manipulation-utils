#Generate a series of test crops for a specified image. Output is autonamed. 
#Two sequences are made, one as a centre crop, zooming in on the image centre, the other gradually removing a side of 
#the image naming it narrower.  

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

def generate_cropped_images(input_path, output_folder='.', prefix='', sequence_type=''):
    img = Image.open(input_path)
    width, height = img.size
    center_x, center_y = width // 2, height // 2

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(max(width, height) // 2):
        # Crop a row and column from the center
        cropped_img = img.crop((max(center_x - i, 0), max(center_y - i, 0), min(center_x + i + 1, width) , min(center_y + i + 1, height)))
        #filename = f"{prefix}_cropsequence{i+1}_{2*i+1}x{2*i+1}.jpg"
        filename = f"{prefix}_cropsequence{i+1}_{min(center_x + i + 1, width)}x{min(center_y + i + 1, height)}.jpg"
        
        # Save the cropped image
        output_path = os.path.join(output_folder, filename)
        cropped_img.save(output_path)
        print(f"Processed: {output_path}")


#leftcrop
    for i in range(width):
            # Crop from the right to achieve 
        cropped_img = img.crop((0, 0, width - i, height))
        filename = f"{prefix}_rightcropsequence{i+1}_{width-i}x{height}.jpg"
        
        # Save the cropped image
        output_path = os.path.join(output_folder, filename)
        cropped_img.save(output_path)

        # Print the filename to stdout
        print(f"Processed: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_test_crops.py input_image_path")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_folder = "."
    prefix = os.path.splitext(os.path.basename(input_image_path))[0]

    generate_cropped_images(input_image_path, output_folder, prefix, sequence_type='crop')
    generate_cropped_images(input_image_path, output_folder, prefix, sequence_type='rightcrop')
