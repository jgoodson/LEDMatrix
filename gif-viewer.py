#!/usr/bin/env python3
import sys
import pickle
import asyncio

import requests
from rgbmatrix import RGBMatrix, RGBMatrixOptions


def swap_image(buffer):
    matrix.SwapOnVSync(buffer)


async def display_frames(frames):
    for frame, delay in frames:
        buffer.SetImage(frame)
        swap_time = loop.time()
        swap_image(buffer)
        swap_duration = loop.time() - swap_time
        #TODO figure out how to trigger exit from this loop
        await asyncio.sleep(delay/100 - swap_duration)


async def loop_forever():
    while running:
        await display_frames(current_frames)

async def monitor_input():
    global current_frames
    while running:
        with open(image_file, 'rb') as i:
            new_gif = pickle.load(i)
        current_frames = new_gif
        await asyncio.sleep(1)

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



