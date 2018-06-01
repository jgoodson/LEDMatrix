import os
import asyncio

from aiohttp import web
import aiohttp_jinja2
import jinja2

routes = web.RouteTableDef()

async def change_image(new_image):
    with open('gif.pickle', 'wb') as o:
        o.write(framesets[new_image])

@routes.post('/upload')
async def store_mp3_handler(request):

    reader = await request.multipart()

    # /!\ Don't forget to validate your inputs /!\

    # reader.next() will `yield` the fields of your form

    field = await reader.next()
    print(field.name)
    assert field.name == 'gif'
    filename = field.filename
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(os.path.join('gifs/', filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))


@routes.post('/change')
async def change(request):
    gif = (await request.post())['gif']
    if gif in framesets:
        await change_image(gif)
        return web.Response(text='Changing to {}'.format(gif))
    else:
        return web.Response(text='Failed to change')

@routes.get('/')
@aiohttp_jinja2.template('index.html')
async def index(request):
    return {'gifs': [gif for gif in framesets.keys()]}


async def update_gifs():
    while True:
        await asyncio.create_subprocess_shell('python3 ParseGIFs.py')
        await asyncio.sleep(5)
        for fs in os.listdir('framesets'):
            bn = fs.rsplit('.', 1)[0]
            if not bn in framesets and fs.endswith('.pickle'):
                with open('framesets/'+fs, 'rb') as i:
                    framesets[bn] = i.read()


if __name__ == '__main__':
    framesets = {}
    for fs in os.listdir('framesets'):
        if fs.endswith('.pickle'):
            with open('framesets/'+fs, 'rb') as i:
                framesets[fs.rsplit('.', 1)[0]] = i.read()

    app = web.Application()
    app.router.add_routes(routes)

    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader('templates'))

    loop = asyncio.get_event_loop()

    asyncio.ensure_future(update_gifs())

    web.run_app(app)
