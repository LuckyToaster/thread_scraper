from os import path, remove, scandir
from pyffmpeg import FFmpeg
from PIL import Image
import asyncio

def get_webm_res(source):
    destination = path.join(path.dirname(source), 'test.png')
    ff = FFmpeg().options(f'-i {source} -vcodec png -ss 10 -vframes 1 -an -f rawvideo {destination}')
    img = Image.open(destination)
    w, h = img.size
    img.close()
    remove(destination)
    return w, h

def roon():
    for file in scandir(source_dir):
        if file.name.endswith('.webm'): 
            print(file.name)
            res = get_webm_res(path.join(source_dir, file.name))
            print(f'{res} {res >= (600, 600)}')
        elif file.name.endswith('.gif'): 
            remove(path.join(source_dir, file.name))

source_dir = "C:\\Users\\sench\\Desktop\\pics"

roon()