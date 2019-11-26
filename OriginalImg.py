import os
import sys
from random import randint
from PIL import Image
import math

def capDimensions(width, height, maxPixels):
    imageSize = math.ceil(math.sqrt(maxPixels)) 
    return (imageSize, imageSize)

def getOriginalColors():
	f=open("/home/marianna/Scrivania/Image-Binary-Converter-master/tool/81_01a81f0196554fc91315263b15ad65b4ca2ac08be2562c219fc87caec1ab564e_i.txt")

	num_methods_i=0
	num_methods_s=0
	index=0
	resultSet=[]
	binaryValues = []

	for line in f:
		first_c = ord(line[0])
		last_c = ord(line[-2])
		lenght_m = len(line)-1
		binaryValues.append(first_c)
		binaryValues.append(last_c)
		binaryValues.append(lenght_m)
		num_methods_i+=1

	while ((index+3)< len(binaryValues)):
		R = binaryValues[index]
		index = index + 1
		G = binaryValues[index]
		index = index + 1
		B = binaryValues[index]
		index = index + 1
		for i in range (0,3000):
		    resultSet.append((R, G, B))
		    
	f=open("/home/marianna/Scrivania/Image-Binary-Converter-master/tool/81_01a81f0196554fc91315263b15ad65b4ca2ac08be2562c219fc87caec1ab564e_s.txt")


	for line in f:
		line = line.split('; ')[-1]
		m = line.split(' ')[0]
		first_c = ord(m[0])
		last_c = ord(m[-2])
		lenght_m = len(m)
		binaryValues.append(first_c)
		binaryValues.append(last_c)
		binaryValues.append(lenght_m)
		num_methods_s+=1


	while ((index+3)< len(binaryValues)):
		R = binaryValues[index] - 100
		index = index + 1
		G = binaryValues[index] + 30
		index = index + 1
		B = binaryValues[index] + 120
		index = index + 1
		for i in range (0,10000):
		    resultSet.append((R, G, B))

	num_pixels= 3000* num_methods_i + 10000 * num_methods_s
	height= 1000
	width= 1000

	if(num_pixels< width*height):
		image = Image.new('RGB', capDimensions(width,height,num_pixels), "black")
		image.putdata(resultSet)
	else:
		image = Image.new('RGB', capDimensions(2*width,2*height,num_pixels), "black")
		image.putdata(resultSet)

	print('Making image...')
	print('Saving image...')
	image.save(sys.argv[1], "PNG")
