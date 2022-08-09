import os, sys
import shutil
from PIL import Image

delete_source = False

# Get source dir
if len(sys.argv) == 1:
    print("Please enter the file name/drag the file you want to convert")
    source = input().strip("\"")
else:
    source = sys.argv[1]

print("Please enter a title")
title = input()
print("Please enter an author")
author = input()

source = os.path.abspath(source)

# Check if source dir is zipped
if os.path.isdir(source):
    imgdir = source
    dir_is_temporary = False
else:
    imgdir = os.path.join(os.path.dirname(source), "temp")
    shutil.unpack_archive(source, imgdir)
    dir_is_temporary = True

# Create pdf
images = []
for root, subfolders, files in os.walk(imgdir):
    for file in files:
        image = Image.open(os.path.join(root, file))
        image = image.convert("RGB")
        images.append(image)

images[0].save(os.path.splitext(source)[0] + ".pdf", save_all=True, append_images=images[1:], title=title, author=author)

# Remove leftover files
if dir_is_temporary:
    shutil.rmtree(imgdir)
if delete_source:
    if os.path.isdir(source):
        shutil.rmtree(source)
    else:
        os.remove(source)
