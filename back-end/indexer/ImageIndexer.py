import os
import io
import argparse
import json
import time
import requests
from requests.exceptions import ConnectionError
from PIL import Image

'''
    ARGUMENT PARSING
'''
parser = argparse.ArgumentParser(description='ImageIndexer')
parser.add_argument('-s', '--source',
                        help='the directory to search for images in, if not set, the whole file system will be scanned',
                        nargs=1, default="\\")
parser.add_argument('-l', '--local',
                    help='Option to save the index locally, takes one parameter: destination for file', nargs=1)

args = parser.parse_args()

'''
    GLOBALS
'''
SOURCE = os.path.abspath(args.source[0])

'''
    Walks through the file system and finds all images.
    
    Returns:
        A list of images, where each image is a dictionary with
        the following fields: filename, path, format, width, height,
        bytes, created, accessed, modified. An empty list if no
        images are found.
'''
def findImages(path=SOURCE):
    images = list()
    for root, folders, files in os.walk(path):
        for f in files:
            if isImage(os.path.join(root,f)):
                imageInfo = getImageInfo(os.path.join(root,f))
                images.append(imageInfo)

    return images

'''
    Writes the image index to a local Json file.

    Args:
        images: A list of images represented as dictionary objects.
    
    Returns:
        A path to the generated/updated file if the write succeeded.
'''
def writeToJsonFile(images):
    jsonFile = os.path.join(args.local[0], 'ImageIndex.json')

    try:
        os.mkdir(os.path.dirname(jsonFile))
    except FileExistsError as e:
        pass
    except PermissionError as e:
        print("ERROR: The program does not have permission ",
              "to create the destination directory: ", os.path.dirname(jsonFile))
    
    try:
        file = open(jsonFile, 'w', encoding='ISO-8859-1')
        file.write("images = " + json.dumps(images))
        file.close()
    except io.UnsupportedOperation as e:
        print("ERROR: Could not write to file.")
    except Exception as e:
        print("ERROR: Something went wrong while writing to file\n", e)

    return jsonFile
    
'''
    A helper functions for checking if a file is a valid image.

    Args:
        filePath: The absolute path to the file.
    
    Returns:
        True if the file is an image, False if not or if it
        can not be determined. 
'''
def isImage(filePath):
    pathIsImage = True
    image = None
    
    try:
        with Image.open(filePath) as img:
            pathIsImage = True
    except OSError as e:
        pathIsImage = False
    except Exception as e:
        pathIsImage = False
    finally:
        if image:
            image.close()
        return pathIsImage
        
'''
    A helper function for creating an image object.

    Args:
        imagePath: The absolute path to the image file.
    
    Returns:
        A dictionary object representing the image.
'''
def getImageInfo(imagePath):
    image       = Image.open(imagePath)
    imageInfo   = dict()
    stats       = os.stat(imagePath)

    imageInfo['filename']   = os.path.basename(image.filename)
    imageInfo['path']       = image.filename
    imageInfo['format']     = image.format
    imageInfo['width']      = image.width
    imageInfo['height']     = image.height
    imageInfo['bytes']      = stats.st_size    
    imageInfo['created']    = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getctime(imagePath)))
    imageInfo['accessed']   = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(stats.st_atime))
    imageInfo['modified']   = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(stats.st_mtime))

    image.close()
    return imageInfo    

if __name__ == "__main__":
    images = findImages()
    
    if args.local:
        jsonFilePath = writeToJsonFile(images)
        print('INFO: The ImageIndex has been saved to ', jsonFilePath)
    else:
        try:
            req = requests.post("http://localhost:4000/images", json=images)
            print("INFO: Response =", req.status_code, req.reason)
        except ConnectionError as e:
            print("ERROR: A connection error occured.\n" +
                  "-Please check if the server you're trying to connect to is running " +
                  "(see README file).")
