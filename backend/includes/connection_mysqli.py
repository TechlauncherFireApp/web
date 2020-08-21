import mysql.connector as mysql
from includes.main import contains

def get():
    conn = None
    try:
        conn = mysql.connect(
            host="localhost",
            user="root",
            password="Fireapp.sem2",
            database="fireapp",
            port="3000",
            charset="utf8",
            autocommit=False
        )
    except:
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