from psycopg2.pool import ThreadedConnectionPool


def delete_comment(db_pool: ThreadedConnectionPool, comment_id: int) -> bool:
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
                DELETE
                FROM comments
                WHERE id = %s
                """,
                    (comment_id,),
                )
                success = True
                conn.commit()
                return success

            else:
                success = False
                return success

    finally:
        db_pool.putconn(conn)
