from commentservice.db.connection import get_conn, release_conn

def create_comment(mod_id: int, author_id: int, text: str) -> int:
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO comments (mod_id, author_id, text)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (mod_id, author_id, text)
            )
            row = cur.fetchone()
            conn.commit()
            return row[0]
    finally:
        release_conn(conn)
