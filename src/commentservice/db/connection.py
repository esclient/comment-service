from psycopg2 import pool
from commentservice.settings import settings

_conn_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=settings.database_url
)

def get_conn():
    return _conn_pool.getconn()

def release_conn(conn):
    _conn_pool.putconn(conn)
