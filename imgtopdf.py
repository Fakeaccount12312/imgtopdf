import os, sys
import shutil
from PIL import Image

delete_sources = False

global images
images = []
global files_with_errors
files_with_errors = []

# To register .cbz and .tar.gz as .tag.gz is split
shutil.register_unpack_format("cbz", [".cbz"], shutil._unpack_zipfile)
known_exts = [".gz"]
for i in shutil.get_unpack_formats():
    known_exts += i[1]

def is_zipped_folder(path):
    name, ext = os.path.splitext(path)
    return ext in known_exts

def read_zipped_folder(path):
    root = os.path.dirname(path)
    name, ext = os.path.splitext(path)

    # Get an unused dir to temporarily use
    tempdir = root
    if not os.path.isdir(os.path.join(root, "temp")):
        tempdir = os.path.join(root, "temp")
    elif not os.path.isdir(name):
        tempdir = name
    else:
        import random, string
        while os.path.isdir(tempdir):
            tempdir = os.path.join(root, "".join([random.choice(string.ascii_letters) for i in range(20)]))

    shutil.unpack_archive(path, tempdir)
    read_folder(tempdir)
    shutil.rmtree(tempdir)


def read_folder(path):
    for root, subdirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            read_file(filepath)

def read_file(path):
    global images
    global files_with_errors
    if is_zipped_folder(path):
        read_zipped_folder(path)
    else:
        try:
            image = Image.open(path)
            image = image.convert("RGB")
            images.append(image)
        except:
            files_with_errors.append(path)


# Get sources
if len(sys.argv) == 1:
    print("Please enter the file name/drag the file you want to convert")
    sources = [input().strip("\"")]
else:
    sources = sys.argv[1:]

print(sources)
print("Please enter a title")
title = input()
print("Please enter an author")
author = input()

# Convert paths to absolute paths
sources = map(os.path.abspath, sources)

# Collect images from sources
for source in sources:
    if os.path.isdir(source):
        read_folder(source)
    else:
        read_file(source)

# Create pdf
images[0].save(os.path.splitext(source)[0] + ".pdf", save_all=True, append_images=images[1:], title=title, author=author)

# Warn if errors occured
if files_with_errors:
    print("Problems with the following files occured:")
    for path in files_with_errors:
        print(path)
    print("A total of " + str(len(files_with_errors)) + " errors occured.")
    input()

# Delete sources
if delete_sources and not files_with_errors:
    for source in sources:
        if os.path.isdir(source):
            shutil.rmtree(source)
        else:
            os.remove(source)
