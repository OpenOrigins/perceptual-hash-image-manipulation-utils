
#Compares a filename full of filename, hashes against a single hash
#python compare.py ./foo/some.hashes 4cb9ad10b2b6c7cc3ac6156baa54152e4d191b66b7e71249b6e69e455cb86935

#Output is differing bits in hamming distance

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
import csv
import sys

def hex_string_diff_bits(hex_str1, hex_str2):
    # Convert hexadecimal strings to binary
    bin_str1 = bin(int(hex_str1, 16))[2:].zfill(len(hex_str1) * 4)
    bin_str2 = bin(int(hex_str2, 16))[2:].zfill(len(hex_str2) * 4)

    # Calculate the number of differing bits
    diff_bits = sum(bit1 != bit2 for bit1, bit2 in zip(bin_str1, bin_str2))
    
    return diff_bits

def compare_hex_strings(csv_file_path, command_line_hex_str):
    results = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header if present

        for row in csv_reader:
            if len(row) >= 2:
                filename, hex_str = row[0], row[1]
                diff_bits = hex_string_diff_bits(command_line_hex_str, hex_str)
                results.append((filename, diff_bits))

    return results

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <csv_file_path> <hex_string>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    command_line_hex_str = sys.argv[2]

    results = compare_hex_strings(csv_file_path, command_line_hex_str)

    for filename, diff_bits in results:
        print(f"Filename: {filename}, Differing Bits: {diff_bits}")

