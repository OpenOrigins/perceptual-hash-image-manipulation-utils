"""OpenOrigins 2024. 
Simple command line utility wrapper around  perception to provide convenient access 
to the various perceptual hash types that it contains for video. 
Licenced for use under the MIT licence"""

from PIL import Image

import imagehash
from perception import hashers, tools
import argparse
import os
import sys


class PerceptualHasher:
    """Tool for computing perceptual hashes of image files (JPEG, PNG, etc.) using multiple different algorithms."""
    PROGNAME = "video-perception.py"
    
    
    @classmethod
    def main(cls, args):
        parser = argparse.ArgumentParser(
            prog=cls.PROGNAME,
            description="Create perceptual hashes for provided files.  "
            + "Supported filetypes for videos are: MOV and MP4. " 
            + "Supported hashes from Perception (NOTE CAPITALISATION!) are FramewiseHasher,TMKL1,TMKL2")
        
        parser.add_argument(
            'hashtype', 
            choices=['FramewiseHasher','TMKL1','TMKL2'])  #Perception

        parser.add_argument(   
            "filename", type=str, help="Filename/path of the file to be processed."
        )

        args = parser.parse_args()

        match (args.hashtype):
  
            case 'FramewiseHasher':
                hash = hashers.FramewiseHasher(hashers.PHash(), interframe_threshold=0.5, frames_per_second=25).compute(args.filename,hash_format="hex")

            case 'TMKL1':
                hash = hashers.TMKL1(hashers.PHashF(),frames_per_second=25,dtype="float32").compute(args.filename,hash_format="hex")

            case 'TMKL2':
                hash = hashers.TMKL2(hashers.PHashF(),frames_per_second=25).compute(args.filename,hash_format="hex")

            case _:
                print("ERROR: Unknown hash type",file=sys.stderr)
        
            print(f"{args.filename}, {hash}, {args.hashtype}")


if __name__ == "__main__":
    PerceptualHasher.main(sys.argv)


