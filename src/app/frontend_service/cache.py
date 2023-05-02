# This file contains all the cache related helper functions

from flask import current_app as app
import json


def get_from_redis(key):
    """
    Description: Helper to retrieve key from cache.
    :param key: string
    :return: value (Any)
    """
    redis_conn = app.redis_connection
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
    redis_conn = app.redis_connection
    if redis_conn:
        if expiry is None:
            expiry = 1 * 60 * 60
        redis_conn.setex(key, expiry, value)
        return value


def get_dict_redis(cache_key):
    """
    Description: Helper to get keys that return dict from cache.
    :param cache_key: string
    :return: value or None(dict)
    """
    value = get_from_redis(cache_key)
    return json.loads(value) if value else None


def set_dict_redis(cache_key, dict_value, expiry):
    """
    Description: Helper to set key with dict value to cache.
    :param cache_key: string
    :param dict_value: dict
    :param expiry: float
    :return: -
    """
    value = json.dumps(dict_value)
    set_in_redis(cache_key, value, expiry)
