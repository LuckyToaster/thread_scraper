from os import path, remove, scandir, makedirs
from requests import get
from re import search
from math import floor
from bs4 import BeautifulSoup
from threading import Thread
from PIL import Image
from argparse import ArgumentParser


def get_hrefs(thread_url):
    request = get(thread_url)
    links = BeautifulSoup(request.content, 'html.parser').find_all('a')
    hrefs = []
    for link in links:
        href = link.get('href')
        if search('^//i.4cdn.org', href): 
            hrefs.append(href) 
    return hrefs


# Jobs for the threads in download
def job(hrefs, directory, verbose):
    for href in hrefs:
        fullpath = path.join(directory, href[-17:])
        with open(fullpath, 'w+b') as f:
            f.write(get('http:' + href).content)
            if verbose: 
                print('https:' + href + ' => ' + fullpath) 


def download(hrefs, directory, verbose, resolution, thread_n):
    if len(hrefs) > thread_n:
        chunk_size = int(floor(len(hrefs) / int(thread_n)))
        remaining_hrefs = len(hrefs) - (thread_n * chunk_size)
        chunked_hrefs = [hrefs[i:i + chunk_size] for i in range(0, len(hrefs), chunk_size)]

        if remaining_hrefs > 0: 
            [chunked_hrefs[i].append(hrefs[(chunk_size * thread_n) + i]) for i in range(remaining_hrefs)]

        threads = [Thread(target=job, args=(chunked_hrefs[i], directory, verbose)) for i in range(thread_n)]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
    else:
        t = Thread(target=job, args=(hrefs, directory, verbose))
        t.start()
        t.join()


def get_media_paths(directory):
    img_paths = []
    for file in scandir(directory):
        if file.is_file() and file.name.endswith(('.jpg', '.png', '.gif', '.webm')):
            img_paths.append(path.join(directory, file.name))
    return img_paths


def filter_by_res(paths, res):
    matches = 0
    for path in paths:
        if path.endswith('.webm'):
            if get_video_resolution(path) < res: remove(path)
            else: matches += 1
        else: 
            img = Image.open(path)
            if img.size < res: 
                img.close()
                remove(path)
            else: matches += 1
    return matches


def get_res_from_arg(str):
    res = str.split('x')
    return int(res[0].strip()), int(res[1].strip())


def get_video_resolution(video_path):
    data = [stream for stream in probe(video_path)["streams"] if stream["codec_type"] == "video"][0]
    return data['width'], data['height']


def mkdir_if_not_exists(path_to_dir):
    if not path.exists(path_to_dir): makedirs(path_to_dir)


def parse_args():
    parser = ArgumentParser(description='Scrapes an imageboard thread and downloads the images.')
    parser.add_argument('thread_url', type=str, help='The URL of the thread to scrape.')
    parser.add_argument('directory', type=str, help='The directory to save the images in.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Prints the URLs of the images as they are downloaded.')
    parser.add_argument('-t', '--threads', type=int, default=5, help='The number of threads to use for downloading. Default is 4.')
    parser.add_argument('-r', '--resolution', type=str, help='The resolution to filter the images by. Default is 0x0.')
    return parser.parse_args()


try:
    if __name__ == '__main__':
        args = parse_args()

        mkdir_if_not_exists(args.directory)
        hrefs = get_hrefs(args.thread_url)
        download(hrefs, args.directory, args.verbose, args.thread_url, args.threads)

        if args.resolution:
            media_paths = get_media_paths(args.directory)
            n_matches = filter_by_res(media_paths, get_res_from_arg(args.resolution))
            if args.verbose:
                print(f"{str(n_matches)}/{str(len(media_paths))} images in {args.directory} meet the resolution requirement")
except ModuleNotFoundError: 
    print(f"Please run the 'setup.py' script to download missing modules, and install this script as an executable") 