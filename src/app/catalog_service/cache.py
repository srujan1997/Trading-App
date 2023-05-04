# This file contains all the cache related helper functions

import redis


def delete_from_redis(key):
    """
    Description: To delete a key from redis
    :param key:
    :return: None
    """
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
