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
    for frame in image.sequence:
        with io.BytesIO() as fp:
            frame.clone().save(fp)
            frameim = PImage.open(fp).convert('RGB')
            frames.append((frameim, frame.delay))
    return pickle.dumps(frames)

if __name__ == '__main__':
    gifs = os.listdir('gifs')
    framesets = {gif: read_image('gifs/'+gif) for gif in gifs}
    for name, gif in framesets.items():
        with open('framesets/{}.pickle'.format(name), 'wb') as o:
            o.write(gif)