from includes.main import contains, error_message
from includes.connection_mysqli import get as connection, is_connected, cur_conn_close, conn_close
import re

def query_mysql(query):
    conn = connection()
    if is_connected(conn):
        cur = conn.cursor()
        try:
            cur.execute(re.sub("\s\s+", " ", query))
            res = [dict(zip(cur.column_names, r)) for r in cur.fetchall()]      # Get all the vehicles inside a request
            
            cur_conn_close(cur, conn)
            return res                                                          # Output
        except Exception as e:
            cur_conn_close(cur, conn)
            raise ConnectionError("Error 0x01: {}".format(e))                   # Fail Message
    
    conn_close(conn)
    raise ConnectionError("Error 0x02")                                         # Fail Message
