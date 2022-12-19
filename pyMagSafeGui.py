#! python3
# pyMagSafeGui.py


import os

from datetime import datetime
import subprocess
from pathlib import Path
import shelve

import pyMagSafeSQLI

# shelve file to save and read magnets DEPRECATED
# no longer generates this folder, this is only used to migrate old data to sqlite
use_shelve = False
folderName = os.path.join('.', 'outFiles')
# os.makedirs(folderName, exist_ok=True)
shelfFilePath = os.path.join(folderName, 'pyMagSafe')

CONFIG_KEY = "config"


# read the configuration saved from previous sessions
# during migration will open and read the shelve file instead
def read_config(migrate=False):
    if migrate:
        with shelve.open(shelfFilePath) as shelfFile:
            config = shelfFile.get(CONFIG_KEY, {})
            return config
    else:
        conn = pyMagSafeSQLI.create_connection()
        config = pyMagSafeSQLI.select_config(conn)
        pyMagSafeSQLI.close_db(conn)
        config_dict = {}
        for key, value in config:
            config_dict[key] = value
        return config_dict


# save the configuration to the database
def save_config(key, value):
    if use_shelve:
        with shelve.open(shelfFilePath) as shelfFile:
            config = shelfFile.get(CONFIG_KEY, {})
            config[key] = value
            shelfFile[CONFIG_KEY] = config
    else:
        conn = pyMagSafeSQLI.create_connection()
        pyMagSafeSQLI.insert_or_replace_config(conn, (key, value))
        pyMagSafeSQLI.close_db(conn)


# read the previously saved magnets
# during migration will open and read the shelve file instead
def read_hist(migrate=False):
    history = {}
    if migrate:
        with shelve.open(shelfFilePath) as shelfFile:
            hist_keys = shelfFile.keys()
            for item in hist_keys:
                if item != CONFIG_KEY:
                    ts = datetime.fromtimestamp(float(item))
                    dt = ts.strftime("%Y-%m-%d %H:%M:%S")
                    history[dt] = shelfFile.get(item)
    else:
        conn = pyMagSafeSQLI.create_connection()
        torrents = pyMagSafeSQLI.select_torrent(conn)
        for key, data, dt in torrents:
            val = history.get(dt, [])
            magnet = pyMagSafeSQLI.select_magnet(conn, {"torrent_id": key})[0][0]
            val.append((data, magnet))
            history[dt] = val
        pyMagSafeSQLI.close_db(conn)
    return history


# read the magnet links from the files in the provided file_list
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


# save the provided magnets to the database
def save_hist(magnets):
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    ts = datetime.timestamp(dt)
    if use_shelve:
        # save magnets with timestamp as key
        with shelve.open(shelfFilePath) as shelfFile:
            shelfFile[str(ts)] = magnets
    else:
        conn = pyMagSafeSQLI.create_connection()
        for torrent, magnet in magnets:
            torr_key = pyMagSafeSQLI.insert_torrent(conn, (torrent,))
            pyMagSafeSQLI.insert_magnet(conn, (magnet, torr_key))
        pyMagSafeSQLI.close_db(conn)


# open all .magnet files in deluge
def send_to_deluge(magnets):
    # open magnet links in deluge
    for magnet in magnets:
        subprocess.run(["deluge", magnet])
