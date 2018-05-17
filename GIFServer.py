import io
import pickle
import os
import asyncio
import sys

import requests
from wand.image import Image as WImage
from PIL import Image as PImage
import aiohttp

def read_image(image_file):
    if image_file.startswith('http://') or image_file.startswith('https://'):
        image = WImage(blob=requests.get(image_file).content)
    else:
        image = WImage(filename=image_file)
    image.resize(32, 32)

    frames = []
    for frame in image.sequence:
        with io.BytesIO() as fp:
            frame.clone().save(fp)
            frameim = PImage.open(fp).convert('RGB')
            frames.append((frameim, frame.delay))
    return pickle.dumps(frames)

async def change_image(new_image):
    with open('gif.pickle', 'wb') as o:
        await o.write(framesets[new_image])

if __name__ == '__main__':
    framesets = {}
    for fs in os.listdir('framesets'):
        if fs.endswith('.pickle'):
            with open(fs, 'rb') as i:
                framesets[fs] = pickle.load(i)
