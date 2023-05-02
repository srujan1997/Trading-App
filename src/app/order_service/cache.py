# This file contains all the cache related helper functions

import os
import redis


def get_redis_connection():
    """
    Description: Helper to establish cache connection.
    :return: cache connection (redis connection object)
    """
    redis_conn = redis.StrictRedis(
        host=os.environ.get("CACHE_URL", "redis"),
        port=6379,
        db=0,
        password=os.environ.get("CACHE_PASSWORD", ""),
        socket_timeout=2,
        socket_connect_timeout=2,
    )

    return redis_conn


def get_from_redis(key):
    """
    Description: Helper to retrieve key from cache.
    :param key: string
    :return: value (Any)
    """
    redis_conn = get_redis_connection()
    if redis_conn:
        value = redis_conn.get(key)
        if value:
            value = value.decode("utf-8")
    return value


def set_in_redis(key, value, expiry=None):
    """
    Description: Helper to set key to cache.
    :param key: string
    :param value: Any
    :param expiry: float
    :return: value (Any)
    """
    redis_conn = get_redis_connection()
    if redis_conn:
        if expiry is None:
            expiry = 1 * 60 * 60
        redis_conn.setex(key, expiry, value)
        return value
