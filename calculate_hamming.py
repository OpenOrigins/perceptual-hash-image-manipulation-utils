#Clustering based on a list of hashes in a text file (filename, hash) and a threshold.  Threshold is the size of the 
#cluster in hamming_distance bits


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

def hamming_distance(hash1, hash2):
    return bin(int(hash1, 16) ^ int(hash2, 16)).count('1')

def find_similar_files(file_path, threshold=10):
    similar_files = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line1 in range(len(lines)):
        filename1, hash1 = lines[line1].strip().split(',')

        found_similar_cluster = False

        for cluster in similar_files:
            if cluster:
                filename2, hash2, _ = cluster[0]

                distance = hamming_distance(hash1, hash2)

                if distance <= threshold:
                    cluster.append((filename1, hash1, distance))
                    found_similar_cluster = True
                    break

        if not found_similar_cluster:
            # If no similar cluster is found, create a new one
            similar_files.append([(filename1, hash1, 0)])  # Initialize with distance 0

    return similar_files

def print_clusters(similar_files):
    for i, cluster in enumerate(similar_files):
        print(f"Cluster {i + 1}:")

        for file_info in cluster:
            if len(file_info) == 3:
                print(f"- {file_info[0]} (Hash: {file_info[1]}, Bits Different: {file_info[2]})")

        print("\n" + "-" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python script.py <file_path> [threshold]")
        sys.exit(1)

    file_path = sys.argv[1]
    threshold = int(sys.argv[2]) if len(sys.argv) == 3 else 10

    similar_files = find_similar_files(file_path, threshold)

    if not similar_files:
        print("No similar files found.")
    else:
        print_clusters(similar_files)

