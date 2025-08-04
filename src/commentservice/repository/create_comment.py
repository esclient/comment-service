from psycopg2.pool import ThreadedConnectionPool


def create_comment(
    db_pool: ThreadedConnectionPool, mod_id: int, author_id: int, text: str
) -> int:
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO comments (mod_id, author_id, text)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (mod_id, author_id, text),
            )
            row = cur.fetchone()
            conn.commit()
            return row[0]
    finally:
        db_pool.putconn(conn)
