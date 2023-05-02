import redis


def delete_from_redis(key):
    redis_conn = redis.StrictRedis(
        host="redis",
        port=6379,
        db=0,
        password="",
        socket_timeout=2,
        socket_connect_timeout=2,
    )
    if redis_conn:
        redis_conn.delete(key)
    return None
