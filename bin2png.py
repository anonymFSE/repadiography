# 5 bytes -> file size

import sys
import math
from random import randint
from PIL import Image

with open(sys.argv[1], 'rb') as in_file:
    print('Reading...')
    data = in_file.read()
    final_size = math.ceil(len(data) / 3) + 5
    dimension = math.ceil(math.sqrt(final_size))
    num_pixels = dimension**2
    print(num_pixels)
    
    print('Making header...')
    header = ''
    b = hex(final_size)[2:]

    if len(b) % 2 == 1:
        b = '0' + b
       
    header = bytes([int(b[i] + b[i-1], 16) for i in range(len(b)-1, -1, -2)])
    
    while len(header) < 5:
        header += bytes([0])

    print('Making data...')
    rgb_data = header
    for byte in data:
        rgb_data += bytes([byte, byte, byte])         
    while len(rgb_data) < num_pixels:
        rgb_data += bytes([0])

    print('Making image...')
    img = Image.frombytes('RGB', (dimension, dimension), rgb_data)
    print('Saving image...')
    img.save(sys.argv[2])
