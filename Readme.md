Quick hacked together Python scripts to display images on an Adafruit 32x32 LED matrix from a Raspberry Pi.

Converts images/gifs to sequence of 32x32 RGB pixel frames and saves them as pickled files.

Runs a webserver (GIFServer.py) which can accept new images or change the current image.

gif-viewer.py uses the rgbmatrix library to update the LED matrix according to the specified image file. Checks constantly for updates to image enabling the webserver to change the displayed image.

Requires Python 3.5+ due to use of asyncio.
