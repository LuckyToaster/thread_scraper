import requests, re 
from os import path, remove, scandir, makedirs
from bs4 import BeautifulSoup as BS
from threading import Thread
from PIL import Image
from sys import argv
from math import floor
from ffmpeg import probe


def get_hrefs(thread_url):
    request = requests.get(thread_url)
    links = BS(request.content, 'html.parser').findAll('a')
    hrefs = []
    for link in links:
        href = link.get('href')
        if re.search('^//i.4cdn.org', href): 
            hrefs.append(href) 
    print('hrefs done')
    return hrefs


def job(hrefs, directory, verbose):
    for href in hrefs:
        fullpath = path.join(directory, href[-17:])
        with open(fullpath, 'w+b') as f:
            f.write(requests.get('http:' + href).content)
            if verbose: 
                print('https:' + href + ' => ' + fullpath) 


def download(hrefs, directory, verbose, thread_n):
    print('downloading ...')
    chunk_size = int(floor(len(hrefs) / thread_n))
    remaining_hrefs = len(hrefs) - (thread_n * chunk_size)
    chunked_hrefs = [hrefs[i:i + chunk_size] for i in range(0, len(hrefs), chunk_size)]

    if remaining_hrefs > 0: 
        [chunked_hrefs[i].append(hrefs[(chunk_size * thread_n) + i]) for i in range(remaining_hrefs)]

    threads = [Thread(target=job, args=(chunked_hrefs[i], directory, verbose)) for i in range(thread_n)]

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


def get_media_paths(directory):
    print('getting media paths')
    img_paths = []
    for file in scandir(directory):
        is_media = (file.name.endswith('.jpg') or file.name.endswith('.png') 
                or file.name.endswith('.gif') or file.name.endswith('.webm'))
        if file.is_file() and is_media: 
            img_paths.append(path.join(directory, file.name))
    return img_paths


def filter_by_res(paths, res):
    print('filtering by res')
    matches = 0
    for path in paths:
        if path.endswith('.webm'):
            if get_vid_resolution(path) < res: 
                remove(path)
        else: 
            img = Image.open(path)
            if img.size < res: remove(path)
            img.close()
        matches += 1
    return matches


def get_video_resolution(video_path):
    print('getting res')
    data = [stream for stream in ffmpeg.probe(video_path)["streams"] if stream["codec_type"] == "video"][0]
    return data['width'], data['height']


def get_res_from_arg(str):
    res = str.split('x')
    return int(res[0].strip()), int(res[1].strip())


def resolution_arg_is_valid():
    if not argv[4].__contains__('x'): return False
    else: return (digit.isdigit() for digit in argv[4].split('x'))


def mkdir_if_not_exists(path_to_dir):
    if not path.exists(path_to_dir): makedirs(path_to_dir)


def args_are_valid():
    return argv[1].__contains__('thread')


def print_help():
    print("\nUSAGE:\n\tthread_scraper.py [URL] [DESTINATION DIRECTORY]\n" +
        "\tthread_scraper.py [URL] [DESTINATION DIRECTORY] [OPTION]...\n" +
        "\tthread_scraper.py [OPTION]\n\n"
        "EXAMPLE:\n" +
        "\tthread_scraper.py https://boards.4chan.org/wg/thread/1234/ C:\\images\\\n\n" +
        "OPTIONS:\n" +
        "\t-r --resolution \tFilter out images smaller than the given resolution\n" +
        "\t-h --help \t\tShow this help message and exit\n" +
        "\t-v --version\n\t-V --verbose\n" +
        "\t-t --threads Number of threads to use for download")


if len(argv) == 1: 
    print_help()
    exit(1)

verbose = False
thread_n = 4
n_matches = 0
media_paths = []

# first check for these flag in args 
for arg in argv:
    if arg == '-V' or arg == '--verbose':
        argv.remove(arg)
        verbose = True
    elif arg == '-h' or arg == '--help':
        argv.remove(arg)
        print_help()
    elif arg == '-v' or arg == '--version':
        argv.remove(arg)
        print("\nThread Scraper version 1.0 LOL\n")

if len(argv) == 3:
    if (args_are_valid()):
        mkdir_if_not_exists(argv[2])
        hrefs = get_hrefs(argv[1])
        download(hrefs, argv[2], verbose, thread_n)
        exit(0)
    else: 
        print("\nERROR: Invalid arguments\n")
        print_help()
        exit(1)
elif len(argv) == 5 and (argv[3] == '-r' or argv[3] == '--resolution'): 
    if args_are_valid() and resolution_arg_is_valid():
        mkdir_if_not_exists(argv[2])
        hrefs = get_hrefs(argv[1])
        download(hrefs, argv[2], verbose, thread_n)
        media_paths = get_media_paths(argv[2])
        n_matches = filter_by_res(media_paths, get_res_from_arg(argv[4]))
    if verbose: 
        print(f"{str(n_matches)}/{str(len(media_paths))} images in '{argv[2]}' meet the resolution requirement")
else: 
    print("\nInvalid resolution format, please try something like: --resolution 1920x1080\nUse --help flag for more info")
    exit(1)

