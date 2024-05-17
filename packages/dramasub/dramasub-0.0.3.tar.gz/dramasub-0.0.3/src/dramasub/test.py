from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
import subprocess
import sys
import os
import re
import shutil
from pathlib import Path

cool_dictionary = {"sharpei": "dog", "persian": "cat", "lop": "rabbit", "golden retriever": "dog"}

print(cool_dictionary["sharpei"])

if "golden retriever" in cool_dictionary:
    try:
        print(int(cool_dictionary["golden retriever"]))
        print("wow robot dog")
    except:
        print("just a normal dog, lame")
