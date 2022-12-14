#! python3

sql_create_torrent_table = """ CREATE TABLE IF NOT EXISTS torrent (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    data text NOT NULL,
                                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                ); """

sql_create_magnet_table = """CREATE TABLE IF NOT EXISTS magnet (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                data text NOT NULL,
                                torrent_id integer NOT NULL,
                                FOREIGN KEY (torrent_id) REFERENCES torrent (id)
                            );"""

sql_create_config_table = """CREATE TABLE IF NOT EXISTS config (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                name text NOT NULL,
                                data text NOT NULL
                            );"""

sql_insert_torrent = """INSERT INTO torrent(data, date)
                        VALUES(?, ?);"""

sql_insert_magnet = """INSERT INTO magnet(data, torrent_id)
                        VALUES(?, ?);"""

sql_insert_config = """INSERT INTO config(name, data)
                        VALUES(?, ?);"""

sql_update_or_replace_config = """insert or replace into config (id, name, data) values (
                                    (select id from config where name = ?), ?, ?);"""
