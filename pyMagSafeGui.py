#! python3
# pyMagSafeGui.py


import os

import subprocess
from pathlib import Path

import pyMagSafeSQLI

# initialize database
pyMagSafeSQLI.create_table(pyMagSafeSQLI.sql_create_config_table)
pyMagSafeSQLI.create_table(pyMagSafeSQLI.sql_create_torrent_magnet_table)


def read_config():
    # read the configuration saved from previous sessions
    # during migration will open and read the shelve file instead
    config = pyMagSafeSQLI.select_config()
    config_dict = {}
    for key, value in config:
        config_dict[key] = value
    return config_dict


def save_config(key, value):
    # save the configuration to the database
    pyMagSafeSQLI.insert_or_replace_config((key, value))


def read_hist(torrent=None):
    # read the previously saved magnets
    # during migration will open and read the shelve file instead
    magnets = []
    if torrent:
        history = pyMagSafeSQLI.select_torrent_magnet(torrent)
    else:
        history = pyMagSafeSQLI.select_torrent_magnet()
    for key, torrent, magnet, date in history:
        magnets.append(Magnet(torrent, magnet, date, key))
    return magnets


def read_magnets(file_list):
    # read the magnet links from the files in the provided file_list
    magnets = []
    # iterating over all files
    for file in file_list:
        if file.endswith(".magnet") and os.path.exists(file):
            # print(file)  # print file name
            with open(file) as f:
                line = f.read()
                mag = Magnet(Path(file).stem, line)
                magnets.append(mag)
                os.remove(file)
    save_hist(magnets)
    return magnets


def save_hist(magnets):
    # save the provided magnets to the database
    for magnet in magnets:
        pyMagSafeSQLI.insert_torrent_magnet((magnet.text, magnet.link))


def send_to_deluge(magnets):
    # open all .magnet files in deluge
    # open magnet links in deluge
    for magnet in magnets:
        subprocess.Popen(["deluge", str(magnet)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class Magnet:
    # object to hold magnets
    def __init__(self, text, link, date=None, id=None):
        self.text = text
        self.link = link
        self.date = date
        self.id = id

    def __str__(self):
        return self.link
