#! python3
# pyMagSafeGui.py


import os

from datetime import datetime
import subprocess
from pathlib import Path

import pyMagSafeSQLI


# read the configuration saved from previous sessions
# during migration will open and read the shelve file instead
def read_config():
    conn = pyMagSafeSQLI.create_connection()
    config = pyMagSafeSQLI.select_config(conn)
    pyMagSafeSQLI.close_db(conn)
    config_dict = {}
    for key, value in config:
        config_dict[key] = value
    return config_dict


# save the configuration to the database
def save_config(key, value):
    conn = pyMagSafeSQLI.create_connection()
    pyMagSafeSQLI.insert_or_replace_config(conn, (key, value))
    pyMagSafeSQLI.close_db(conn)


# read the previously saved magnets
# during migration will open and read the shelve file instead
def read_hist():
    magnets = []
    conn = pyMagSafeSQLI.create_connection()
    torrents = pyMagSafeSQLI.select_torrent(conn)
    for key, data, dt in torrents:
        magnet = pyMagSafeSQLI.select_magnet(conn, {"torrent_id": key})[0][0]
        magnets.append(Magnet(data, magnet, dt))
    pyMagSafeSQLI.close_db(conn)
    return magnets


# read the magnet links from the files in the provided file_list
def read_magnets(file_list):
    ts = datetime.now()
    dt = ts.strftime("%Y-%m-%d %H:%M:%S")
    magnets = []
    # iterating over all files
    for file in file_list:
        if file.endswith(".magnet") and os.path.exists(file):
            # print(file)  # print file name
            with open(file) as f:
                line = f.read()
                mag = Magnet(Path(file).stem, line, dt)
                magnets.append(mag)
                os.remove(file)
    save_hist(magnets)
    return magnets


# save the provided magnets to the database
def save_hist(magnets):
    conn = pyMagSafeSQLI.create_connection()
    for magnet in magnets:
        torr_key = pyMagSafeSQLI.insert_torrent(conn, (magnet.text, magnet.date))
        pyMagSafeSQLI.insert_magnet(conn, (magnet.link, torr_key, magnet.date))
    pyMagSafeSQLI.close_db(conn)


# open all .magnet files in deluge
def send_to_deluge(magnets):
    # open magnet links in deluge
    for magnet in magnets:
        subprocess.run(["deluge", magnet])


class Magnet:
    def __init__(self, text, link, date):
        self.text = text
        self.link = link
        self.date = date

    def __str__(self):
        return self.text
