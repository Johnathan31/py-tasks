from .connection import pool


def get_connection():
    with pool.connection() as connection:
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
