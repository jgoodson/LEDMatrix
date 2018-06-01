#!/usr/bin/env python3
import os
import pickle
import io

import requests
from wand.image import Image as WImage
from PIL import Image as PImage

def read_image(image_file):
    if image_file.startswith('http://') or image_file.startswith('https://'):
        image = WImage(blob=requests.get(image_file).content)
    else:
        image = WImage(filename=image_file)
    image.resize(32, 32)

    frames = []
    try:
        for frame in image.sequence:
            with io.BytesIO() as fp:
                frame.clone().save(fp)
                frameim = PImage.open(fp).convert('RGB')
                frames.append((frameim, frame.delay))
        return pickle.dumps(frames)
    except OSError:
        return None

if __name__ == '__main__':
    gifs = os.listdir('gifs')
    completed = [fs.rsplit('.')[0] for fs in os.listdir('framesets')]
    framesets = {gif: read_image('gifs/'+gif) for gif in gifs if not gif.rsplit('.')[0] in completed}
    for name, gif in framesets.items():
        if gif:
            with open('framesets/{}.pickle'.format(name), 'wb') as o:
                o.write(gif)