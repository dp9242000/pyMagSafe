# pyMagSafe
pyMageSafe is both a text based interface and a GUI script for sending .magnet files to deluge. 
.magnet files are files with a single line containing a magnet link for use with torrent applications. 
pyMagSafe will remove the files automatically and store them in a database to allow the user to resend them to deluge later.

pyMageSafe will generate a sqlite folder to contain the database file for storing the history of .magnet files and app configuration.
