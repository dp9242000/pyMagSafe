#! python3
# pyMagSafe.py
# usage: python3 pyMagSafe.py <-h> <-l> <key>
# if no options provided, pyMagSafe.py will read all .magnet files in the same directory and send them to deluge

import os
import shelve
import sys
from datetime import datetime
import subprocess

# Getting the current date and time
dt = datetime.now()

# getting the timestamp
ts = datetime.timestamp(dt)

folderName = os.path.join('.','outFiles')
os.makedirs(folderName, exist_ok = True)
magnets = []
# giving file extension
ext = '.magnet'

# open shelf file to save and read magnets
shelfFilePath = os.path.join(folderName, 'pyMagSafe')
shelfFile = shelve.open(shelfFilePath)

if len(sys.argv) >= 2:
    # print usage
    if sys.argv[1] == "-h":
        print("usage: python3 pyMagSafe.py <-h> <-l> <key>")
        print("if no options provided, pyMagSafe.py will read all .magnet files in the same directory and send them to deluge")
    # user entered "-l" to request list of keys/timestamps
    elif sys.argv[1] == "-l":
        keys = list(shelfFile.keys())
        keys.sort()
        max = len(max(keys, key = len))
        for item in keys:
            timestamp = float(item)
            datetime = datetime.fromtimestamp(timestamp)
            print(f'{item :<{max}} : {datetime}')
    # user entered a time stamp to request previous magnets
    elif sys.argv[1] in list(shelfFile.keys()):
        for item in list(shelfFile.get(sys.argv[1])):
            print(f"{item[0]} :\n{item[1]}")
            print()

# no argmunets given, open all .magnet files in deluge
else:
    # iterating over all files
    for files in os.listdir(os.path.join('.')):
        if files.endswith(ext):
            print(files)  # printing file name of desired extension
            with open(files) as f:
                line = f.read()
                magnets.append((files, line))
                os.remove(files)

    # save magnets with timestamp as key
    shelfFile[str(ts)] = magnets


    # open magnet links in deluge
    for magnet in magnets:
        subprocess.run(["deluge", magnet[1]])

# close the shelf file
shelfFile.close()