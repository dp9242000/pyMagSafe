#! python3
# pyMagSafeSQLI.py
# SQLite interface for pyMagSafeGui

import logging

from PySide6.QtSql import QSqlDatabase, QSqlQuery

import os

logging.basicConfig(level=logging.ERROR)


# first create db folder if it doesn't exist
database = "db"
folder_path = "~/.config/pyMagSafe/sqlite"
folder_path = os.path.expanduser(folder_path)
os.makedirs(folder_path, exist_ok=True)
db_file_path = os.path.join(folder_path, database)

conn = QSqlDatabase.addDatabase("QSQLITE")
conn.setDatabaseName(db_file_path)

# sql statements to create tables
sql_create_torrent_magnet_table = """CREATE TABLE IF NOT EXISTS torrent_magnet (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                torrent text NOT NULL,
                                magnet text NOT NULL,
                                create_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                update_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );"""

sql_create_config_table = """CREATE TABLE IF NOT EXISTS config (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL,
                                data text NOT NULL,
                                create_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                update_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );"""


def create_table(create_table_sql):
    # at database connection: conn, create table using the provided sql statement
    # creates a table using the create_table_sql statement in the database at conn
    logging.info(f"Creating table")
    logging.debug(f"{create_table_sql}")
    conn.open()
    query = QSqlQuery()
    query.exec(create_table_sql)
    conn.close()


def insert_torrent_magnet(data):
    # insert data into torrent_magnet table
    if len(data) == 2:
        sql = f"INSERT INTO torrent_magnet(torrent, magnet) VALUES(\'{data[0]}\', \'{data[1]}\');"
    else:
        sql = f"""INSERT INTO torrent_magnet(torrent, magnet, create_dt) 
        VALUES(\'{data[0]}\', \'{data[1]}\', \'{data[2]}\');"""
    logging.info(f"inserting into torrent_magnet table")
    logging.debug(f"{sql}")
    conn.open()
    query = QSqlQuery()
    query.exec(sql)
    conn.close()


def select_torrent_magnet(torrent=None):
    # select from the torrent table
    tor_mag = []
    if torrent is None:
        torrent = {}
    if torrent.get("id"):
        t = torrent.get("id")
        sql = f"select id, torrent, magnet, datetime(create_dt, \'localtime\') from torrent_magnet where id={t};"
    else:
        sql = f"select id, torrent, magnet, datetime(create_dt, \'localtime\') from torrent_magnet;"
    logging.info(f"selecting from torrent_magnet table")
    logging.debug(f"{sql}")
    conn.open()
    query = QSqlQuery()
    query.exec(sql)
    # tor_mag.append((query.value(1), query.value(2), query.value(3)))
    while query.next():
        tor_mag.append((query.value(0), query.value(1), query.value(2), query.value(3)))
    conn.close()
    return tor_mag


def insert_config(config):
    # insert into the config table
    # insert data into config table
    sql = f"INSERT INTO config(name, data) VALUES(\'{config[0]}\', \'{config[1]}\');"
    logging.info(f"inserting into config table")
    logging.debug(f"{sql}")
    conn.open()
    query = QSqlQuery()
    query.exec(sql)
    conn.close()


def insert_or_replace_config(config):
    # insert or replace into the config table
    # insort or replace data in config table
    if len(config) == 2:
        sql = f"""insert or replace into config (id, name, data) values ((select id from config where name = 
        \'{config[0]}\'), \'{config[0]}\', \'{config[1]}\');"""
    else:
        sql = f"""insert or replace into config (id, name, data, create_dt) values ((select id from config where name =
         \'{config[0]}\'), \'{config[0]}\', \'{config[1]}\', \'{config[2]}\');"""
    logging.info(f"insert or replace into config table")
    logging.debug(f"{sql}")
    conn.open()
    query = QSqlQuery()
    query.exec(sql)
    conn.close()


def select_config():
    # select from the config table, returns a dictionary with name as key, and data as value
    config = {}
    sql = f"select name, data from config;"
    logging.info(f"select config data from config table")
    logging.debug(f"{sql}")
    conn.open()
    query = QSqlQuery()
    query.exec(sql)
    conn.close()
    while query.next():
        config[query.value(0)] = query.value(1)
    conn.close()
    return config
