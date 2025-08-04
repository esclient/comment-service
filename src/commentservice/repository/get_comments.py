from psycopg2.pool import ThreadedConnectionPool


def get_comments(db_pool: ThreadedConnectionPool, mod_id: int) -> tuple:
    conn = db_pool.getconn()
    comments = ()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, author_id, text, created_at, edited_at
                FROM comments
                WHERE mod_id = %s
                """,
                (mod_id,),
            )
            comments = cur.fetchall()
            return comments
    finally:
        db_pool.putconn(conn)
