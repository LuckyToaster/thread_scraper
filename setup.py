#!/usr/bin/env python
import subprocess, sys
from setuptools import setup, find_packages

# implement pip as a subprocess:
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "bs4"])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "PIL"])
    print("\nSET-UP COMPLETED SUCCESSFULLY\n")
except: print("\n SET-UP FAILED SUCCESSFULLY\n")

setup_info = dict(
    name='threadscrape',
    version=info['version'],
    author='Lucky Toaster',
    url='https://github.com/LuckyToaster/thread_scraper/',
    download_url='https://github.com/LuckyToaster/thread_scraper/',
    project_urls={
        'Documentation': 'https://github.com/LuckyToaster/thread_scraper/',
        'Source': 'https://github.com/pyglet/pyglet',
        'Tracker': 'https://github.com/pyglet/pyglet/issues',
    },
    description='Cross-platform windowing and multimedia library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package info
    packages=['pyglet'] + ['pyglet.' + pkg for pkg in find_packages('pyglet')],

    # Add _ prefix to the names of temporary build dirs
    options={'build': {'build_base': '_build'}, },
    zip_safe=True,
)

setup(**setup_info)