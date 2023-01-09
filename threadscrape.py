import requests, re, sys, os
from os import path, remove, scandir, makedirs
from bs4 import BeautifulSoup as BS
from pyffmpeg import FFmpeg
from PIL import Image

def download(url, destination_path, verbose):
    request = requests.get(url)
    links = BS(request.content, 'html.parser').findAll('a') # a link is a <a> tag
    for link in links:
        href = link.get('href') 
        if re.search('^//i.4cdn.org', href):
            fullpath = path.join(destination_path, href[-17:])
            with open(fullpath, 'w+b') as f:
                f.write(requests.get('http:' + href).content)
                if verbose: print('https:' + href + ' => ' + fullpath) 

def get_media_paths(directory):
    img_paths = []
    for file in scandir(directory):
        # is this even necessary?
        is_media = file.name.endswith('.jpg') or file.name.endswith('.png') or file.name.endswith('.gif') or file.name.encode('.webm')
        if file.is_file() and is_media: 
            img_paths.append(os.path.join(directory, file.name))
    return img_paths

def filter_by_res(img_paths, res):
    match_n = 0
    for path in img_paths:
        if path.endswith('.webm') and get_webm_res(path) < res: 
            remove(path)
        else:
            img = Image.open(path)
            if img.size[0] < res[0] or img.size[1] < res[1]:
                img.close()
                remove(path)
            else: match_n += 1
    return match_n

def get_webm_res(webm_path):
    destination = path.join(path.dirname(webm_path), 'test.png')
    ff = FFmpeg().options(f'-i {webm_path} -vcodec png -ss 10 -vframes 1 -an -f rawvideo {destination}')
    img = Image.open(destination)
    w, h = img.size
    img.close()
    remove(destination)
    return w, h

def get_res_from_argument(str):
    res = str.split('x')
    return [int(res[0].strip()), int(res[1].strip())]

def prepare_path(path):
    if not os.path.exists(path): os.makedirs(path)

def args_are_valid():
    return sys.argv[1].__contains__('thread') and (sys.argv[2].__contains__('\\') or sys.argv[2].__contains__('/'))

def resolution_arg_is_valid():
    if not sys.argv[4].__contains__('x'): return False
    else: return (digit.isdigit() for digit in sys.argv[4].split('x'))

def get_res(str):
    res = str.split('x')
    return [int(res[0].strip()), int(res[1].strip())]

def print_help():
    print("\nUSAGE:\n\tthread_scraper.py [URL] [DESTINATION DIRECTORY]\n" +
        "\tthread_scraper.py [URL] [DESTINATION DIRECTORY] [OPTION]...\n" +
        "\tthread_scraper.py [OPTION]\n\n"
        "EXAMPLE:\n" +
        "\tthread_scraper.py https://boards.4chan.org/wg/thread/1234/ C:\\images\\\n\n" +
        "OPTIONS:\n" +
        "\t-r --resolution \tFilter out images smaller than the given resolution\n" +
        "\t-h --help \t\tShow this help message and exit\n" +
        "\t-v --version\n\t-V --verbose\n")


if len(sys.argv) == 1: 
    print_help()
    exit(1)

verbose = False

# first check for these flag in args 
for arg in sys.argv:
    if arg == '-V' or arg == '--verbose':
        sys.argv.remove(arg)
        verbose = True
    elif arg == '-h' or arg == '--help':
        sys.argv.remove(arg)
        print_help()
    elif arg == '-v' or arg == '--version':
        sys.argv.remove(arg)
        print("\nThread Scraper version 1.0 LOL\n")

"""
c = 0
while (len(sys.argv)) > 3:
    if sys.argv[c] == '-V' or sys.argv[c] == '--verbose':
        sys.argv.pop(c)
        verbose = True
    elif sys.argv[c] == '-h' or sys.argv[c] == '--help':
        print_help()
        sys.argv.pop(c)
    elif sys.argv[c] == '-v' or sys.argv[c] == '--version':
        print("\nThread Scraper version 1.0 LOL\n")
        sys.argv.pop(n)
    c += 1
"""

if len(sys.argv) == 3:
    if (args_are_valid()):
        prepare_path(sys.argv[2])
        download(sys.argv[1], sys.argv[2], verbose)
        exit(0)
    else: 
        print("\nERROR: Invalid arguments\n")
        print_help()
        exit(1)
elif len(sys.argv) == 5 and (sys.argv[3] == '-r' or sys.argv[3] == '--resolution'): 
    if args_are_valid() and resolution_arg_is_valid():
        prepare_path(sys.argv[2])
        download(sys.argv[1], sys.argv[2], verbose)
        media_paths = get_media_paths(sys.argv[2])
        n_matches = filter_by_res(media_paths, get_res(sys.argv[4]))
        if verbose: 
            print(f"{str(n_matches)}/{str(len(media_paths))} images in '{sys.argv[2]}' meet the resolution requirement")
    else: 
        print("\nInvalid resolution format, please try something like: --resolution 1920x1080\nUse --help flag for more info")
        exit(1)