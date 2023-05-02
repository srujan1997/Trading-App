from flask import current_app as app
import json


def get_from_redis(key):
    redis_conn = app.redis_connection
    if redis_conn:
        value = redis_conn.get(key)
        if value:
            value = value.decode("utf-8")
    return value


def set_in_redis(key, value, expiry=None):
    redis_conn = app.redis_connection
    if redis_conn:
        if expiry is None:
            expiry = 1 * 60 * 60
        redis_conn.setex(key, expiry, value)
        return value


def get_dict_redis(cache_key):
    value = get_from_redis(cache_key)
    return json.loads(value) if value else None


def set_dict_redis(cache_key, dict_value, expiry):
    value = json.dumps(dict_value)
    set_in_redis(cache_key, value, expiry)
