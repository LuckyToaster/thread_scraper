import os
import re
import urllib.request
import requests
from bs4 import BeautifulSoup

def get_hrefs(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    a_tags = soup.find_all('a')
    hrefs = [a['href'] for a in a_tags if 'href' in a.attrs]
    #return [a.get('href') for a in a_tags if a.get('href')]
    return hrefs


def download_media(hrefs, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for href in hrefs:
        # Check if the href is a valid media file (e.g. ends with .jpg, .mp4, etc.)
        if re.search(r'\.(jpg|jpeg|png|gif|mp4|mov|webm|mkv)$', href):
            try:
                # Download the media file
                filename = os.path.join(download_path, os.path.basename(href))
                urllib.request.urlretrieve(href, filename)
                print(f'Successfully downloaded {filename}')
            except urllib.error.HTTPError as e:
                print(f'Error: {e}')


import sysconfig
print(sysconfig.get_path("include"))
