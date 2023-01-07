#!/usr/bin/env python
import subprocess, sys
from setuptools import setup, find_packages

# implement pip as a subprocess:
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "bs4"])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pillow"])
    print("\nSET-UP COMPLETED SUCCESSFULLY\n")
except: print("\n SET-UP FAILED SUCCESSFULLY\n")
