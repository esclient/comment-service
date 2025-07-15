from commentservice.db.connection import get_conn, release_conn

def get_comments(mod_id: int) -> int:
    conn = get_conn()
    comments = ()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, author_id, text, created_at
                FROM comments
                WHERE mod_id = %s
                """,
                (mod_id,)
            )
            comments = cur.fetchall()
            return comments
    finally:
        release_conn(conn)
