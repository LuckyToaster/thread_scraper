#!/usr/bin/env python
import subprocess, sys
from setuptools import setup, find_packages

modules = ['bs4', 'pillow', 'pyffmpeg', 'numba']

# implement pip as a subprocess:
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "bs4"])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pillow"])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pyffmpeg"])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'argparse'])
    print("\nSET-UP COMPLETED SUCCESSFULLY\n")
except: print("\n SET-UP FAILED SUCCESSFULLY\n")
