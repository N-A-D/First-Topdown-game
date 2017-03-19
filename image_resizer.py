'''
@author: Ned Austin Datiles
'''
import PIL
from PIL import Image
import os
from os import path

def resize_images(directory):
    print("Starting resize operation")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                resize(path.join(root, file))
            
    print('finished resizing all png files')
    
def resize(name, base_width=128):
    image = Image.open(name)
    width_percent = (base_width/float(image.size[0]))
    h_size = int(float(image.size[1]) * float(width_percent))
    image = image.resize((base_width, h_size), PIL.Image.ANTIALIAS)
    image.save(name)

#resize_images('img\\Player animations')
