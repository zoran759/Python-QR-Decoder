# Python-QR-Decoder-Encoder
A very basic QR Decoder and Encoder written in python. The decoding process begins by modifying the image so that it removes all white space outside of the QR Code and scales it to a 1 block to pixel ratio. After that, it removes the mask placed on the QR code. From that point on, the demasked QR code is then traversed. This traversal is then broken up into 8 bits and processed. Currently, this application can only decode and works only with binary and QR versions less than 4. More work will be added to complete this.

# Libraries
This requires PIL (Python Image Library). To install, type the following command on terminal:
```sudo pip install http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz```

# How to Use
In the commandline of this directory, type: ```python QRMatrix.py decode samples/test.png```

# To Do
Create the encoding feature and program the Reed–Solomon Error Correction algorithm. Doing the latter will allow for the decoding of > version 4 QR codes. 

# Error Detection Algorithm Guide
http://www.thonky.com/qr-code-tutorial/structure-final-message
