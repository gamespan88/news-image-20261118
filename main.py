#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261118.

Writes the entry image to /output/entry.png. The image ships in this
repository as entry.png (drawn by build_image.py); this program copies
it byte for byte, so both runs produce identical output.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
