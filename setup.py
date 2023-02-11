#!/usr/bin/env python
import subprocess, sys

modules = ['bs4', 'pillow', 'pyffmpeg', 'requests', 'pyinstaller']

try:
    [subprocess.check_call([sys.executable, '-m', 'pip', 'install', module]) for module in modules]
    print("DEPENDENCIES SUCCESSFULLY INSTALLED")
except: print("\nDEPENDENCIES COULDN'T BE INSTALLED\n")

try:
    subprocess.run(['pyinstaller', '--onefile', 'threadscrape.py'])
    print("\nEXECUTABLE SUCCESFULLY COMPILED\n")
except: print("COMPILATION FAILED\n")