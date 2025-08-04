from psycopg2.pool import ThreadedConnectionPool


def edit_comment(
    db_pool: ThreadedConnectionPool, comment_id: int, text: str
) -> bool:
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM comments
                WHERE id = %s
                """,
                (comment_id,),
            )

            comment = cur.fetchone()
            if comment:
                cur.execute(
                    """
                    UPDATE comments
                    SET text = %s, edited_at = NOW()
                    WHERE id = %s
                    """,
                    (text, comment_id),
                )

                conn.commit()

                success = True
            else:
                success = False
            return success
    finally:
        db_pool.putconn(conn)
