#!/usr/bin/env python
import subprocess, sys, os

modules = ['bs4', 'pillow', 'pyffmpeg', 'requests', 'pyinstaller']
downloaded_deps, compiled = False, False

try:
    [subprocess.check_call([sys.executable, '-m', 'pip', 'install', module]) for module in modules]
    print("DEPENDENCIES SUCCESSFULLY INSTALLED")
    downloaded_deps = True
except: print("\nDEPENDENCIES COULDN'T BE INSTALLED\n")

if downloaded_deps:
    try:
        subprocess.run(['pyinstaller', '--onefile', 'threadscrape.py'])
        print("\nEXECUTABLE SUCCESFULLY COMPILED\n")
        compiled = True
    except: print("\nCOMPILATION FAILED\n")

if compiled:
    try:
        executable_path = os.path.join(os.getcwd(), '\\dist\\')

        if executable_path not in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + executable_path
            subprocess.call('setx PATH "%s"' % os.environ['PATH'], shell=True)
        print('\nEXECUTABLE ADDED TO PATH')
    except: print('\nEXECUTABLE COULD NOT BE ADDED TO PATH')