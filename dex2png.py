# 5 bytes -> file size

import os
import sys
import math
import cv2
from random import randint
from PIL import Image
import PIL

def capDimensions(width, height, maxPixels):
    pixels = width * height
    #ratio = float(width) / height
    imageSize = int(math.ceil(math.sqrt(maxPixels)))
    #height2 = math.ceil(float(height) / (scale))
    #width2 = math.ceil(ratio * height / (scale))
    print(imageSize) 
    return (imageSize, imageSize)

with open(sys.argv[1], 'rb') as in_file:
    data=in_file.read()
    binaryValues=[]
    resultSet=[]
    index=0

    for byte in data:
        binaryValues.append(byte)

 
    while(index<len(binaryValues)):
        R= ord(binaryValues[index])
        G= ord(binaryValues[index])
        B= ord(binaryValues[index]) 
        index=index+1
        resultSet.append((R,G,B))
    
    num_pixels= index
    height= 1000
    width= 1000
        
  
image = Image.new('RGB',capDimensions(1000,1000, num_pixels), "black")
image.putdata(resultSet)


print('Making image...')
print('Saving image...')


image.save(sys.argv[2], "PNG")



