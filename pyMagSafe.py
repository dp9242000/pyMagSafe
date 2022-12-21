#! python3
# pyMagSafe.py
# usage: python3 pyMagSafe.py <path> <-h> <-l> <-k id>
# if no options provided, pyMagSafe.py will read all .magnet files in the same directory and send them to deluge

import os
import sys

import pyMagSafeGui


def absolute_file_paths(directory):
    file_paths = []
    for file in os.listdir(directory):
        if file.endswith(".magnet"):
            file_paths.append(os.path.abspath(os.path.join(directory, file)))
            print(os.path.abspath(os.path.join(directory, file)))
    return file_paths


if sys.argv[1] == "-h":  # print usage
    print("usage: python3 pyMagSafe.py <path> <-h> <-l> <key>")
    print("pyMagSafe will read all .magnet files in the <path> directory and send them to deluge")

elif sys.argv[1] == "-l":  # user entered "-l" to request list of keys/timestamps
    magnets = pyMagSafeGui.read_hist()
    for magnet in magnets:
        print(f"{magnet.id} - {magnet.text}")

elif sys.argv[1] == "-k" and sys.argv[2]:
    print(f"resending torrent id: {sys.argv[2]}")
    torrent = {"id": sys.argv[2]}
    magnets = pyMagSafeGui.read_hist(torrent)
    pyMagSafeGui.send_to_deluge(magnets)

else:  # no arguments given, open all .magnet files in deluge
    path = sys.argv[1]
    print(f"reading magnet files in path: {path}")
    if os.path.exists(path):
        magnets = pyMagSafeGui.read_magnets(absolute_file_paths(path))
        for magnet in magnets:
            print(f"sending: {magnet.text}")
        # open magnet links in deluge
        pyMagSafeGui.send_to_deluge(magnets)
