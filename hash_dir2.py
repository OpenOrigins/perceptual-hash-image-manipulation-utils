#!/usr/bin/env python

# This utility will generate a pdq hash for all files in the specified directory.  
#Usage and output is in the format 

#python ThreatExchange/pdq/python/pdqhashing/tools/hash_dir2.py images/ | tee allthehashes.hashes
#images/camera_12F95B0C-1C0A-481C-B992-17242108DC1D-jpeg-SCALE50-QUALITY90.jpeg,722c6f7c6a29d281c2c73b512b7cae1ea82ae5c3a56b1d7c9592c4922d687b6a
#images/hawker_fury_meme-jpeg-SCALE50-QUALITY90.jpeg,9e1eec4746f111b9318b9c0e6e36e3e7c6718d1839ce70c60e628f39b03167ce
#images/hawker_fury_horizontalflip-bmp-SCALE50.bmp,8b4bb3161b244cece4de8959336336b29324d84d6c9125b35b37da6ce56c349b
#images/hawker_fury_horizontalflip-jpeg-SCALE30-QUALITY90.jpeg,8b4bb3161b244cece4de8959336336b29324d84d6c9125b35b37da6ce56c349b
#images/hawker_fury_subtleairbrush-jpeg-SCALE70-QUALITY80.jpeg,9e1ee6474ef131b9318b9c0c6e36e3e7c6718f1839c470c60e628f39b039e1ce
#images/camera_12F95B0C-1C0A-481C-B992-17242108DC1D-gif-SCALE30.gif,ccb9ad10b2b6c7cc32c6146baa54172ecd191a66b7e61249b6e69e555cb86935
#images/hawker_fury-gif-SCALE60.gif,9e1ee6474ef131b9318b9c0c6e36e3e7c6718f1839c670c60e628f39b031e1ce
#images/hawker_fury-jpeg-SCALE10-QUALITY2.jpeg,9e1ee6474ef131f9318b9c0c6e36e3e7c6718d18398c70c60e628f39b039e1ce
#images/hawker_fury_meme-jpeg-SCALE5-QUALITY5.jpeg,9e1eecc31ef131b9318b8c0c6e76e7e3c6719d1831ce70c60e728f39a03163ce
#images/camera_12F95B0C-1C0A-481C-B992-17242108DC1D-jpeg-SCALE90-QUALITY60.jpeg,722c6f7c6a29d281c2c73b512b7cae1ea82ae5c3a56b1d7c9592c4922d687b6a
#images/hawker_fury_meme-jpeg-SCALE90-QUALITY60.jpeg,9e1eec4746f111b9318b9c0e6e36e3e7c6718d1839ce70c60e628f39b03167ce
#images/hawker_fury-jpeg-SCALE40-QUALITY30.jpeg,9e1ee6474ef111b9318b9c0c6e36e3e7c6718f1839ce70c60e628f39b031e1ce
#images/hawker_fury_horizontalflip-gif-SCALE5.gif,824bb33659a44cecc4de9a59332336b69364d84d6d9325b35b27da6ce56c2493
#images/hawker_fury_subtleairbrush-jpeg-SCALE30-QUALITY10.jpeg,9e1ee6474ef131b9318b9c0c6e36e3e7c6718d1839c670c60e628f39b039e1ce
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


This utility merely wraps a comvenient function from the pdq software part of threat exchange 
https://github.com/facebook/ThreatExchange that originates from Meta/Facebook and use of this is covered by
a BSD license https://github.com/facebook/ThreatExchange/blob/main/LICENSE.  

"""

import argparse
import os
import sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from pdqhashing.hasher.pdq_hasher import PDQHasher
from pdqhashing.types.hash256 import Hash256

class PDQPhotoHasherTool:
    """Tool for computing PDQ hashes of image files (JPEG, PNG, etc.)."""

    PROGNAME = "hash_dir2"

    class Context:
        """Helper class for tracking image-to-image deltas"""

        numPDQHash = int()
        pdqHashPrev = Hash256()
        hadError = bool()

        def __init__(self, _numPDQHash, _pdqHashPrev, _hadError) -> None:
            self.numPDQHash = _numPDQHash
            self.pdqHashPrev = _pdqHashPrev
            self.hadError = _hadError

    @classmethod
    def main(cls, args):
        parser = argparse.ArgumentParser(
            prog=cls.PROGNAME,
            description="Create PDQ Photo hashes for provided files. "
            + "Supported filetypes are: GIF, TGA, BMP, JPEG and PNG.",
        )

        parser.add_argument(
            "directory", type=str, help="Directory containing files to be processed."
        )

        args = parser.parse_args()

        pdqHasher = PDQHasher()
        context = cls.Context(0, None, False)

        for filename in os.listdir(args.directory):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png','.gif','.bmp','.tga')):
                if not filename.lower().startswith('._'):
                    file_path = os.path.join(args.directory, filename)
                    #print(f"#1  About to process filename ", file_path)
                    cls.processFile(pdqHasher, file_path, context)

    @classmethod
    def processFile(cls, pdqHasher, filename, context):
        #print(f"#2  About to process filename ", filename)

        hashAndQuality = pdqHasher.fromFile(filename)
        #print(f"#3  Just processed to process filename ", filename)

        if hashAndQuality is None or hashAndQuality.getHash() is None:
            sys.stderr.write(
                "{}: could not compute hash for image file {}\n".format(
                    cls.PROGNAME, filename
                )
            )
            exit(1)

        hash = hashAndQuality.getHash()

        # Extract quality and scale from the filename using a regular expression
        match = re.search(r'quality_(\d+)_scale_(\d+)', filename)
        quality = int(match.group(1)) if match and match.group(1) else None
        scale = int(match.group(2)) if match and match.group(2) else None

        # Format the quality and scale as two-digit numbers
        formatted_quality = f"{quality:02d}" if quality is not None and 0 <= quality <= 9 else None
        formatted_scale = f"{scale:02d}" if scale is not None and 0 <= scale <= 9 else None

        # Update the filename with quality and scale percentages
        if formatted_quality is not None and formatted_scale is not None:
            new_filename = f"{filename}_{formatted_quality}_{formatted_scale}"
            print(f"{new_filename},{hash}")
        else:
            print(f"{filename},{hash}")

        context.pdqHashPrev = hash

if __name__ == "__main__":
    PDQPhotoHasherTool.main(sys.argv)
