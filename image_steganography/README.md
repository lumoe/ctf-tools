# Steganography

The encoding script encodes a string into an image file by manipulating the LSB of the first channel.  
It appends ```_encoded``` to the encoded image file and shows a visual difference of the images.

Usage for encoding:  
```$ python3 encode.py path_to_image text_to_encode```

Usage for decoding:  
```$ python3 decode.py path_to_image```