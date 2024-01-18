#Give it a directory, will hash everything in it and then try to cluster similar things using colours!  
#Let it run for a while will take a while. 

"""
Copyright 2023 vOpenOrigins 2023

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

import os
from PIL import Image
import imagehash
from sklearn.cluster import DBSCAN
from collections import defaultdict

def compute_hashes(directory):
    image_hashes = {}
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(directory, filename)
            img = Image.open(image_path)
            # Resize the image for faster processing (optional)
            img = img.resize((8, 8))
            # Compute perceptual hash using average hash
            phash = imagehash.average_hash(img)
            image_hashes[filename] = str(phash)
    return image_hashes

def find_clusters(image_hashes, threshold=8, min_samples=2):
    filenames_by_cluster = defaultdict(list)

    # Convert hashes to numerical arrays
    hash_values = list(image_hashes.values())
    hash_arrays = [[int(hash_value, 16)] for hash_value in hash_values]

    # Cluster similar images using DBSCAN
    clustering = DBSCAN(eps=threshold, min_samples=min_samples).fit(hash_arrays)

    # Group filenames by cluster
    for filename, label in zip(image_hashes.keys(), clustering.labels_):
        filenames_by_cluster[label].append(filename)

    return filenames_by_cluster

def print_colored_clusters(clusters):
    color_mapping = {
        0: '\033[91m',  # Red
        1: '\033[92m',  # Green
        2: '\033[93m',  # Yellow
        3: '\033[94m',  # Blue
        4: '\033[95m',  # Purple
        5: '\033[96m',  # Cyan
        6: '\033[97m',  # White
    }

    for cluster_id, filenames in clusters.items():
        color_code = color_mapping[cluster_id % len(color_mapping)]
        print(f"{color_code}Cluster {cluster_id + 1}:\033[0m {filenames}")

def main(directory):
    image_hashes = compute_hashes(directory)
    clusters = find_clusters(image_hashes)

    # Print colored clusters
    print_colored_clusters(clusters)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python cluster_images.py <directory>")
        sys.exit(1)

    directory_path = sys.argv[1]
    main(directory_path)

