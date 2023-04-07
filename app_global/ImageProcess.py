from PIL import Image
import os

def Resize_Image(image):
    print(os.path.abspath(image.name))
    im = Image.open(os.path.abspath(image.name))
    required_height = 310
    required_width = int(required_height / image.height * image.width)
    print(width)
    new_size = im.resize(required_width,required_height)
    