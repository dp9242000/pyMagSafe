#! python3
# pyMagSafeSQLI.py
# SQLite interface for pyMagSafeGui

import pyMagSafeGui

from pysqlite3 import dbapi2 as sqlite3
from pysqlite3 import Error

import os

# first create db folder if it doesn't exist
database = "db"
folder_path = os.path.abspath(os.path.join('.', 'sqlite'))
os.makedirs(folder_path, exist_ok=True)
db_file_path = os.path.join(folder_path, database)

# sql statements to create tables
sql_create_torrent_table = """ CREATE TABLE IF NOT EXISTS torrent (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    data text NOT NULL,
                                    create_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    update_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                ); """

sql_create_magnet_table = """CREATE TABLE IF NOT EXISTS magnet (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                data text NOT NULL,
                                torrent_id integer NOT NULL,
                                create_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                update_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (torrent_id) REFERENCES torrent (id)
                            );"""

sql_create_config_table = """CREATE TABLE IF NOT EXISTS config (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL,
                                data text NOT NULL,
                                create_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                update_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );"""


def create_connection(db=db_file_path):
    # use the supplied file path to connect to the database
    # creates new if not exist
    # create a database connection to the SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db)
        # print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def close_db(conn):
    # close the database connection at conn
    # closes the database at conn
    if conn:
        try:
            conn.close()
        except Error as e:
            print(e)


def create_table(conn, create_table_sql):
    # at database connection: conn, create table using the provided sql statement
    # creates a table using the create_table_sql statement in the database at conn
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_torrent(conn, torrent):
    # insert into the torrent table
    # insert data into torrent table
    if len(torrent) == 1:
        sql = f"INSERT INTO torrent(data) VALUES(\'{torrent[0]}\');"
    else:
        sql = f"INSERT INTO torrent(data, create_dt) VALUES(\'{torrent[0]}\', \'{torrent[1]}\');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def update_torrent(conn, torrent_key, torrent):
    # update into the torrent table
    # insort or replace data in config table
    sql = f"update torrent set data = {torrent}, update_dt = CURRENT_TIMESTAMP where id = {torrent_key};"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def select_torrent(conn, torrent=None):
    # select from the torrent table
    if torrent is None:
        torrent = {}
    if torrent.get("id"):
        t = torrent.get("id")
        sql = f"select id, data, datetime(create_dt, \'localtime\') from torrent where id={t};"
    elif torrent.get("data"):
        t = torrent.get("data")
        sql = f"select id, data, datetime(create_dt, \'localtime\') from torrent where data={t};"
    else:
        sql = f"select id, data, datetime(create_dt, \'localtime\') from torrent;"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def insert_magnet(conn, magnet):
    # insert into the magnet table
    # insert data into magnet table
    if len(magnet) == 2:
        sql = f"INSERT INTO magnet(data, torrent_id) VALUES(\'{magnet[0]}\', \'{magnet[1]}\');"
    else:
        sql = f"INSERT INTO magnet(data, torrent_id, create_dt) VALUES(\'{magnet[0]}\', \'{magnet[1]}\', \'{magnet[2]}\');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def update_magnet(conn, torrent_key, magnet):
    # update into the magnet table
    # insort or replace data in config table
    sql = f"update magnet set data = {magnet}, update_dt = CURRENT_TIMESTAMP where torrent_id = {torrent_key};"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def select_magnet(conn, magnet):
    # select from the magnet table
    if magnet.get("id"):
        m = magnet.get("id")
        sql = f"select data from magnet where id={m};"
    elif magnet.get("torrent_id"):
        m = magnet.get("torrent_id")
        sql = f"select data from magnet where torrent_id={m};"
    else:
        sql = "select data from magnet;"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def insert_config(conn, config):
    # insert into the config table
    # insert data into config table
    sql = f"INSERT INTO config(name, data) VALUES(\'{config[0]}\', \'{config[1]}\');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def insert_or_replace_config(conn, config):
    # insert or replace into the config table
    # insort or replace data in config table
    if len(config) == 2:
        sql = f"insert or replace into config (id, name, data) values (" \
              f"(select id from config where name = \'{config[0]}\'), \'{config[0]}\'," \
              f" \'{config[1]}\');"
    else:
        sql = f"insert or replace into config (id, name, data, create_dt) values (" \
              f"(select id from config where name = \'{config[0]}\'), \'{config[0]}\'," \
              f" \'{config[1]}\', \'{config[2]}\');"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def select_config(conn):
    # select from the config table
    sql = f"select name, data from config;"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
