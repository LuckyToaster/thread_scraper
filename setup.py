#!/usr/bin/env python
from cx_Freeze import setup, Executable
import subprocess, sys 

modules = ['bs4', 'pillow', 'pyffmpeg', 'cython', 'cx_Freeze']
compile_to_c_command = "cython threadscrape.pyx --embed"
generate_binary_command = ""

# install dependencies
try:
    [subprocess.check_call([sys.executable, '-m', 'pip', 'install', module]) for module in modules]
    print("\nSET-UP COMPLETED SUCCESSFULLY\n")
except: print("\n SET-UP FAILED SUCCESSFULLY\n")


# trying to make the executable:
try:
    setup(
        name = "YourScript",
        version = "0.1",
        description = "Your script description",
        executables = [Executable("threadscrape.pyd")]
    )
    print("\nEXECUTABLE COMPILED SUCCESSFULLY")
except: print("\nEXECUTABLE CREATION FAILED")

"""
# compile to C
try:
    comp = subprocess.run(compile_to_c_command, stdout=subprocess.PIPE, shell=True)
    print(comp.stdout.decode())
    print('\nCOMPILATION COMPLETED SUCCESSFULLY')
except: print("\nCOMPILATION FAILED SUCCESSFULLY")

# buld executable 
try:
   executable = subprocess.run(generate_binary_command, stdout=subprocess.PIPE, shell=True) 
   print(executable.stdout.decode())
   print('\nEXECUTABLE GENERATED SUCCESSFULLY')
except: print('\nBINARY CREATION FAILED')
"""