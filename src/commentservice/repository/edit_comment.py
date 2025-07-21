from commentservice.db.connection import get_conn, release_conn


def edit_comment(comment_id: int, text: str) -> bool:
    conn = get_conn()
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
        release_conn(conn)
