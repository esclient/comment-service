from commentservice.db.connection import get_conn, release_conn


def delete_comment(comment_id: int) -> int:
    conn = get_conn()
    try:
        with conn.cursor() as cur:

            cur.execute(
                """
                SELECT *
                FROM comments
                WHERE id = %s
                """,
                (comment_id,)
            )
            comment = cur.fetchone()

            if comment:

                cur.execute(
                """
                DELETE 
                FROM comments
                WHERE id = %s
                """,
                (comment_id,)
                )
                success = True
                conn.commit()
                return success
            
            else:
                success = False
                return success
            
    finally:
        release_conn(conn)
