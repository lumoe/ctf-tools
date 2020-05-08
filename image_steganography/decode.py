import os
import sys

from PIL import Image

STOP_BYTE = 0x06

def decode_from_image(img):
    data = ''
    for vPixel in range(img.height):
        for hPixel in range(img.width):
            pixel = img.getpixel((vPixel, hPixel))
            
            # Only the first byte of the channel is used
            if type(pixel) != int:
                pixel = pixel[0]

            data += str(pixel & 0x01)

    out = ''
    for value in range(0, len(data), 8):
        v = int('0b' + data[value:value+8], 2)
        if v == STOP_BYTE:
            break

        out += chr(v)
    
    return out

def help_message():
    return """
usage: decode.py image_file 

Decodes embedded message from an image file by reading the LSB of each pixel

positional arguments:
 image_file  path to image file with text encoded
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(help_message())
        exit(-1)

    img = Image.open(sys.argv[1])
    print(f"Message found: {decode_from_image(img)}")

