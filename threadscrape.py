import requests, os, re, sys 
from bs4 import BeautifulSoup as BS
from PIL import Image

def prepare_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_valid(href):
    return re.search('^//i.4cdn.org', href)

def download(url, path, verbose):
    request = requests.get(url)
    links = BS(request.content, 'html.parser').findAll('a') # a link is a <a> tag
    for link in links:
        href = link.get('href') 
        if is_valid(href):
            fullpath = path + '/' + href[-17:]
            with open(fullpath, 'w+b') as f:
                f.write(requests.get('http:' + href).content)
                if verbose:
                    print('https:' + href + ' => ' + fullpath) # log

def get_img_paths(directory):
    img_paths = []
    for file in os.scandir(directory):
        is_media = file.name.endswith('.jpg') or file.name.endswith('.png') or file.name.endswith('.gif') or file.name.encode('.webm')
        if file.is_file() and is_img:
            img_paths.append(os.path.join(directory, file.name))
    return img_paths

def filter_by_res(img_paths, res):
    match_n = 0
    for path in img_paths:
        img = Image.open(path)
        if img.size[0] < res[0] or img.size[1] < res[1]:
            img.close()
            os.remove(path)
        else: match_n += 1
    return match_n

def get_res_from_argument(str):
    res = str.split('x')
    return [int(res[0].strip()), int(res[1].strip())]

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

verbose = False

# first check for these flag in args 
for n in range(len(sys.argv)):
    if sys.argv[n] == '-V' or sys.argv[n] == '--verbose':
        sys.argv.pop(n)
        verbose = True
    if (sys.argv[n] == '-h' or sys.argv[n] == '--help'):
        print_help()
        sys.argv.pop(n)
    elif (sys.argv[n] == '-v' or sys.argv[n] == '--version'):
        print("\nThread Scraper version 1.0 LOL\n")
        sys.argv.pop(n)

if len(sys.argv) == 3:
    if (args_are_valid()):
        prepare_path(sys.argv[2])
        download(sys.argv[1], sys.argv[2], verbose)
        exit(0)
    else: 
        print_help()
        exit(1)
elif len(sys.argv) == 5 and (sys.argv[3] == '-r' or sys.argv[3] == '--resolution'): 
    if resolution_arg_is_valid():
        prepare_path(sys.argv[2])
        download(sys.argv[1], sys.argv[2], verbose)
        img_paths = get_img_paths(sys.argv[2])
        n_matches = filter_by_res(img_paths, get_res(sys.argv[4]))
        if verbose: print(f"{str(n_matches)}/{str(len(img_paths))} images in '{sys.argv[2]}' meet the resolution requirement")
    else: 
        print("\nInvalid resolution format, please try something like: --resolution 1920x1080\nUse --help flag for more info")
        exit(1)