#! python3
# pyMagSafeGui.py

import os
import shelve
from datetime import datetime
import subprocess
from pathlib import Path

folderName = os.path.join('.', 'outFiles')
os.makedirs(folderName, exist_ok=True)

# open shelf file to save and read magnets
shelfFilePath = os.path.join(folderName, 'pyMagSafe')

CONFIG_KEY = "config"


def read_config():
    with shelve.open(shelfFilePath) as shelfFile:
        config = shelfFile.get(CONFIG_KEY, {})
        return config


def save_config(key, value):
    with shelve.open(shelfFilePath) as shelfFile:
        config = shelfFile.get(CONFIG_KEY, {})
        config[key] = value
        shelfFile[CONFIG_KEY] = config


def read_hist():
    history = {}
    with shelve.open(shelfFilePath) as shelfFile:
        hist_keys = shelfFile.keys()
        for item in hist_keys:
            if item != CONFIG_KEY:
                ts = datetime.fromtimestamp(float(item))
                dt = ts.strftime("%Y-%m-%d %H:%M:%S")
                history[dt] = shelfFile.get(item)
    return history


def read_magnets(file_list):
    magnets = []
    # iterating over all files
    for file in file_list:
        if file.endswith(".magnet") and os.path.exists(file):
            # print(file)  # print file name
            with open(file) as f:
                line = f.read()
                magnets.append((Path(file).stem, line))
                os.remove(file)
    save_hist(magnets)
    return magnets


def save_hist(magnets):
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)

    # save magnets with timestamp as key
    with shelve.open(shelfFilePath) as shelfFile:
        shelfFile[str(ts)] = magnets


# open all .magnet files in deluge
def send_to_deluge(magnets):
    # open magnet links in deluge
    for magnet in magnets:
        subprocess.run(["deluge", magnet])
