#!/usr/bin/env python3
import sys
import pickle
import asyncio
import os.path

import requests
from rgbmatrix import RGBMatrix, RGBMatrixOptions


def swap_image(buffer):
    matrix.SwapOnVSync(buffer)

async def display_frames(frames):
    global interrupted
    interrupted = False
    for frame, delay in frames:
        if interrupted:
            break
        buffer.SetImage(frame)
        swap_time = loop.time()
        swap_image(buffer)
        swap_duration = loop.time() - swap_time
        if delay:
            await asyncio.sleep(delay/100 - swap_duration)
        else:
            await asyncio.sleep(1)


async def loop_forever():
    while running:
        await display_frames(current_frames)

async def monitor_input():
    global current_frames, interrupted
    last_updated = os.path.getmtime(image_file)
    while running:
        if last_updated != os.path.getmtime(image_file):
            try:
                with open(image_file, 'rb') as i:
                    new_gif = pickle.load(i)
                current_frames = new_gif
                interrupted = True
                last_updated = os.path.getmtime(image_file)
            except:
                pass
        await asyncio.sleep(.1)



if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit("Require an image argument")
    else:
        image_file = sys.argv[1]

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1

    matrix = RGBMatrix(options=options)
    buffer = matrix.CreateFrameCanvas()

    loop = asyncio.get_event_loop()
    running = True

    with open(image_file, 'rb') as i:
        current_frames = pickle.load(i)

    asyncio.ensure_future(loop_forever())
    asyncio.ensure_future(monitor_input())


    try:
        loop.run_forever()
    finally:
        loop.close()



