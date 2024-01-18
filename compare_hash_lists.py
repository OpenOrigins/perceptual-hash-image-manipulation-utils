
#Compares two lists of hashes.  
#Syntax of the lists is just 2 column text file 
#filename1, hash1
#filename2, hash2
#...
#The filenames are only used to idnetify the hashes suggest that you use descriptive filenaes!

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
import sys
from itertools import product

def hamming_distance(hash1, hash2):
    # Compute the Hamming distance between two binary strings
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))

def load_hashes(file_path):
    # Load perceptual hashes from a text file
    hash_dict = {}
    with open(file_path, 'rb') as file:
        for line in file:
            line = line.decode('utf-8').strip()
            filename, hash_str = line.split(',')
            hash_dict[filename] = hash_str
    return hash_dict

def compare_hashes(file1_hashes, file2_hashes, threshold):
    # Compare hashes and output pairs below the threshold
    for (filename1, hash1), (filename2, hash2) in product(file1_hashes.items(), file2_hashes.items()):
        distance = hamming_distance(hash1, hash2)
        if distance < threshold:
            print(f"{filename1} - {filename2}: Hamming Distance = {distance} bits")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python compare_hashes.py file1.txt file2.txt threshold")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    threshold = int(sys.argv[3])

    # Load perceptual hashes from the two files
    file1_hashes = load_hashes(file1_path)
    file2_hashes = load_hashes(file2_path)

    # Compare hashes and output pairs below the threshold
    compare_hashes(file1_hashes, file2_hashes, threshold)
