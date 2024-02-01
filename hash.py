"""OpenOrigins 2024. 
Simple command line utility wrapper around ImageHash and Perception to provide convenient access 
to the various perceptual hash types that it contains. 
Licenced for use under the MIT licence"""

from PIL import Image
import imagehash
from perception import hashers, tools
import argparse
import os
import sys


class PerceptualHasher:
    """Tool for computing perceptual hashes of image files (JPEG, PNG, etc.) using multiple different algorithms."""
    PROGNAME = "hash.py"
    
    
    @classmethod
    def main(cls, args):
        parser = argparse.ArgumentParser(
            prog=cls.PROGNAME,
            description="Create perceptual hashes for provided files.  "
            + "Supported filetypes for iamges are: JPEG and PNG. " 
            + "Supported hashes from ImageHash are average_hash,colorhash,crop_resistant_hash,dhash,phash,phash_simple,whash"
            + "Supported hashes from Perception (NOTE CAPITALISATION!) are AverageHash, MarrHildreth, BlockMean, DHash, ColorMoment, PHash, PHashF, PHashU8, WaveletHash")
        
        parser.add_argument(
            'hashtype', 
            choices=['average_hash', 'average', 'colorhash', 'color', 'colourhash','colour', #Imagehash
                'crop_resistant_hash','crop','crop_resistant','dhash','phash','phash_simple','whash',#Imagehash
                'AverageHash', 'MarrHildreth', 'BlockMean', 'DHash', 'ColorMoment', #Perception
                'PHash', 'PHashF', 'PHashU8', 'WaveletHash'])  #Perception

        parser.add_argument(   
            "filename", type=str, help="Filename/path of the file to be processed."
        )

        args = parser.parse_args()

        match (args.hashtype):
            case  "average_hash" | "average":
                hash = imagehash.average_hash(Image.open(args.filename))
                
            case "colorhash" | "color" | "colour" | "colourhash":
                hash = imagehash.colorhash(Image.open(args.filename))
                
            case "crop_resistant_hash" | "crop_resistant"| "crop":
                hash = imagehash.crop_resistant_hash(Image.open(args.filename))
                
            case "dhash":
                hash = imagehash.dhash(Image.open(args.filename))
                
            case "dhash_vertical":
                hash = imagehash.dhash_vertical(Image.open(args.filename))
                
            case "phash":
                hash = imagehash.phash(Image.open(args.filename))
                
            case "phash_simple":
                hash = imagehash.phash_simple(Image.open(args.filename))
                
            case "whash":
                hash = imagehash.whash(Image.open(args.filename))
                
            case 'AverageHash':
                hash = hashers.AverageHash().compute(Image.open(args.filename),hash_format="hex")
            case 'MarrHildreth':
                hash = 'ERROR BROKEN IN CV2'
                #hash = hashers.MarrHildreth().compute(Image.open(args.filename),hash_format="hex")
            case 'BlockMean':
                hash = 'ERROR BROKEN IN CV2'
                #hash = hashers.BlockMean().compute(Image.open(args.filename),hash_format="hex")
            case 'DHash':
                hash = hashers.DHash(hash_size=8).compute(Image.open(args.filename),hash_format="hex")
                #NOTE Doesn't match the imagehash dhash version. 
            case 'ColorMoment':
                hash = 'ERROR BROKEN IN CV2'
                #hash = hashers.ColorMoment().compute(Image.open(args.filename),hash_format="hex")
            case 'PHash':
                hash = hashers.PHash().compute(Image.open(args.filename),hash_format="hex")
            case 'PHashF':
                hash = hashers.PHashF().compute(Image.open(args.filename),hash_format="hex")
            case 'PHashU8':
                hash = hashers.PHashU8().compute(Image.open(args.filename),hash_format="hex")
            case 'WaveletHash':
                hash = hashers.WaveletHash().compute(Image.open(args.filename),hash_format="hex")
            case _:
                print("ERROR: Unknown hash type",file=sys.stderr)
        
        print(args.filename,',',hash,',',args.hashtype)


if __name__ == "__main__":
    PerceptualHasher.main(sys.argv)
