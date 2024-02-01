from PIL import Image
import imagehash
from perception import hashers, tools
import argparse
import os
import sys
import glob

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
            "path", type=str, help="Directory path of the files to be processed."
        )

        args = parser.parse_args()

        # Find all files matching the pattern
        file_paths = glob.glob(os.path.join(args.path, '*'))
        
        for file_path in file_paths:
            # Process each file
            hash = None
            try:
                # Compute hash based on the selected type
                match args.hashtype:
                    case 'FramewiseHasher':
                        hash = hashers.FramewiseHasher(hashers.PHash(), interframe_threshold=0.5, frames_per_second=25).compute(file_path, hash_format="hex")
                    case 'TMKL1':
                        hash = hashers.TMKL1(hashers.PHashF(), frames_per_second=25, dtype="float32").compute(file_path, hash_format="hex")
                    case 'TMKL2':
                        hash = hashers.TMKL2(hashers.PHashF(), frames_per_second=25).compute(file_path, hash_format="hex")
                    case _:
                        print("ERROR: Unknown hash type",file=sys.stderr)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                continue

            print(f"{file_path}, {hash}, {args.hashtype}")

if __name__ == "__main__":
    PerceptualHasher.main(sys.argv)
