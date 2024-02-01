from PIL import Image
import imagehash
from perception import hashers, tools
import argparse
import os
import sys

class PerceptualHasher:
    """Tool for computing perceptual hashes of image files (JPEG, PNG, etc.) using multiple different algorithms."""
    PROGNAME = "hash-dir.py"
    
    @classmethod
    def main(cls, args):
        parser = argparse.ArgumentParser(
            prog=cls.PROGNAME,
            description="Create perceptual hashes for provided files.  "
            + "Supported filetypes for images are: JPEG and PNG. " 
            + "Supported hashes from ImageHash are average_hash, colorhash, crop_resistant_hash, dhash, phash, phash_simple, whash"
            + "Supported hashes from Perception (NOTE CAPITALIZATION!) are AverageHash, MarrHildreth, BlockMean, DHash, ColorMoment, PHash, PHashF, PHashU8, WaveletHash")
        
        parser.add_argument(
            'hashtype', 
            choices=['average_hash', 'average', 'colorhash', 'color', 'colourhash','colour', # Imagehash
                     'crop_resistant_hash','crop','crop_resistant','dhash','phash','phash_simple','whash', # Imagehash
                     'AverageHash', 'MarrHildreth', 'BlockMean', 'DHash', 'ColorMoment', # Perception
                     'PHash', 'PHashF', 'PHashU8', 'WaveletHash'])  # Perception

        parser.add_argument(   
            "path", type=str, help="Directory path of the files to be processed."
        )

        args = parser.parse_args()

        for filename in os.listdir(args.path):
            filepath = os.path.join(args.path, filename)
            if os.path.isfile(filepath):
                try:
                    hash = None
                    match args.hashtype:
                        case "average_hash" | "average":
                            hash = imagehash.average_hash(Image.open(filepath))
                        case "colorhash" | "color" | "colourhash" | "colour":
                            hash = imagehash.colorhash(Image.open(filepath))
                        case "crop_resistant_hash" | "crop_resistant"| "crop":
                            hash = imagehash.crop_resistant_hash(Image.open(filepath))
                        case "dhash":
                            hash = imagehash.dhash(Image.open(filepath))
                        case "phash":
                            hash = imagehash.phash(Image.open(filepath))
                        case "phash_simple":
                            hash = imagehash.phash_simple(Image.open(filepath))
                        case "whash":
                            hash = imagehash.whash(Image.open(filepath))
                        case 'AverageHash':
                            hash = hashers.AverageHash().compute(Image.open(filepath), hash_format="hex")
                        case 'MarrHildreth':
                            hash = 'ERROR BROKEN IN CV2'
                        case 'BlockMean':
                            hash = 'ERROR BROKEN IN CV2'
                        case 'DHash':
                            hash = hashers.DHash(hash_size=8).compute(Image.open(filepath), hash_format="hex")
                        case 'ColorMoment':
                            hash = 'ERROR BROKEN IN CV2'
                        case 'PHash':
                            hash = hashers.PHash().compute(Image.open(filepath), hash_format="hex")
                        case 'PHashF':
                            hash = hashers.PHashF().compute(Image.open(filepath), hash_format="hex")
                        case 'PHashU8':
                            hash = hashers.PHashU8().compute(Image.open(filepath), hash_format="hex")
                        case 'WaveletHash':
                            hash = hashers.WaveletHash().compute(Image.open(filepath), hash_format="hex")
                        case _:
                            print("ERROR: Unknown hash type",file=sys.stderr)
                    
                    print(f"{filepath}, {hash}, {args.hashtype}")
                except Exception as e:
                    print(f"Error processing file {filepath}: {e}")

if __name__ == "__main__":
    PerceptualHasher.main(sys.argv)
