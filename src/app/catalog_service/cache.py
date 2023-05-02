from flask import current_app as app


def delete_from_redis(key):
    redis_conn = app.redis_connection
    if redis_conn:
        redis_conn.delete(key)
    return None
