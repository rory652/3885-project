import redis
from time import time


class Database(dict):
    def __init__(self, host, port, database=0, password=None, expires=3600):
        self._connection = redis.StrictRedis(host=host, port=port, db=database, password=password, decode_responses=True)

        # Check the connection - improve later
        self._connection.ping()

        # Time in seconds for the cached data to expire - defaults to 1 hour
        self._expires = expires

        super().__init__()

    def __getitem__(self, key):
        if super().__contains__(key):
            data = super().__getitem__(key)

            if time() < data["expires"]:
                return data["value"]

            super().__delitem__(key)

        if self._connection.exists(key):
            data = self._connection.hgetall(key)

            super().__setitem__(key, {"value": data, "expires": time() + self._expires})
            return data

        return None

    def __setitem__(self, key, value):
        self._connection.hset(key, mapping=value)

        # Cache new data
        super().__setitem__(key, {"value": value, "expires": time() + self._expires})

        return True

    def __delitem__(self, key):
        self._connection.delete(key)
        super().__delitem__(key)

    def __contains__(self, key):
        return self._connection.exists(key)

    def iterator(self, pattern="*"):
        return self._connection.scan_iter(pattern)

    def test(self):
        return self._connection.ping()
