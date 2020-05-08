import os
import sys

from PIL import Image, ImageChops

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
STOP_BYTE = 0x06

def encode_data(data, img):
    i = 0
    for vPixel in range(img.height):
        for hPixel in range(img.width):
            if(i == len(data)):
                break
            
            pixel = img.getpixel((vPixel, hPixel))

            # Use only the first byte of the channel
            _pixel = 0
            if type(pixel) != int:
                pixel = list(pixel)
                _pixel = pixel[0]
            
            # Update pixel
            _pixel = (_pixel & ~0x01) | int(data[i])
            
            if type(pixel) != int:
                pixel[0] = _pixel
            else:
                pixel = _pixel

            img.putpixel((vPixel, hPixel), tuple(pixel))
            i += 1
    
    return img


def prepare_data(data):
    bin_data = []
    # Append padded bytes
    for char in data:
        bin_data += format(ord(char), '#010b')[2:]

    # Append stop byte
    bin_data += format(STOP_BYTE, '#010b')[2:]
    return bin_data

def help_message():
    return """
usage: encode.py image_file text

Encodes the provided text into the image 
file by manipulating the LSB of the pixel values

positional arguments:
 image_file  path to image file
 text        string to encode into the image file
"""

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(help_message())
        exit(-1)

    data = prepare_data(sys.argv[2])

    img = Image.open(sys.argv[1])
    img_encoded = encode_data(data, img.copy())
    img_encoded.save(f"{sys.argv[1].split('.')[0]}_encoded.{sys.argv[1].split('.')[-1]}")

    diff = ImageChops.difference(img_encoded, img)
    diff.show()