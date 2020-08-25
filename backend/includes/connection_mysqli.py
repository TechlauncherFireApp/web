import mysql.connector as mysql
from includes.main import contains
import os

def get():
    conn = None
    try:
        conn = mysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=os.getenv("MYSQL_PORT"),
            charset="utf8",
            autocommit=False
        )
    except mysql.Error as err:
        print("Something went wrong: {}".format(err))
        return False
    finally:
        if is_connected(conn): return conn
        else: return False

def is_connected(conn):
    try: return conn and contains(conn) and conn.is_connected()
    except: return False

def cur_conn_close(cur, conn):
    try: cur.close()
    except: cur = None

    try:
        if is_connected(conn): conn.close()
    except: conn = None