from os import path, remove, scandir
from pyffmpeg import FFmpeg
from PIL import Image
import asyncio
import ffmpeg, pprint 

def roon(directory):
    for file in scandir(directory):
        if file.name.endswith('.webm'): 
            res = get_webm_res(path.join(directory, file.name))
            print(f'{res} {res >= (600, 600)}')
        elif file.name.endswith('.gif'): 
            remove(path.join(source_dir, file.name))

source_dir = "C:\\Users\\sench\\Videos\\aussies"
src_dir = "C:\\Users\\sench\\Videos\\aussies\\lez.webm"

def get_webm_res(path):
    data = [stream for stream in ffmpeg.probe(path)["streams"] if stream["codec_type"] == "video"][0]
    return data['width'], data['height']


roon(source_dir)
