from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from commentservice.repository.model import Comment


def get_comments(
    db_pool: ThreadedConnectionPool, mod_id: int
) -> list[Comment]:
    conn = db_pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, author_id, text, created_at, edited_at
                FROM comments
                WHERE mod_id = %s
                """,
                (mod_id,),
            )
            return [Comment(**row) for row in cur.fetchall()]
    finally:
        db_pool.putconn(conn)
