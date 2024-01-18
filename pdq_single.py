#!/usr/bin/env python


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


This utility merely exposes a comvenient function from the pdq software part of threat exchange 
https://github.com/facebook/ThreatExchange that originates from Meta/Facebook and use of this is covered by
a BSD license https://github.com/facebook/ThreatExchange/blob/main/LICENSE.  

"""



import argparse
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from pdqhashing.hasher.pdq_hasher import PDQHasher
from pdqhashing.types.hash256 import Hash256


class PDQPhotoHasherTool:
    """Tool for computing PDQ hashes of image files (JPEG, PNG, etc.)."""

    PROGNAME = "PDQPhotoHasherTool"

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
            + "Supported filetypes are: JPEG and PNG.",
        )

        parser.add_argument(
            "filename", type=str, help="Filename/path of the file to be processed."
        )

        args = parser.parse_args()

        pdqHasher = PDQHasher()
        context = cls.Context(0, None, False)
        cls.processFile(pdqHasher, args.filename, context)

    @classmethod
    def processFile(cls, pdqHasher, filename, context):
        hashAndQuality = pdqHasher.fromFile(filename)

        if hashAndQuality is None or hashAndQuality.getHash() is None:
            sys.stderr.write(
                "{}: could not compute hash for image file {}\n".format(
                    cls.PROGNAME, filename
                )
            )
            exit(1)

        hash = hashAndQuality.getHash()
        print(hash)
        context.pdqHashPrev = hash

if __name__ == "__main__":
    PDQPhotoHasherTool.main(sys.argv)
