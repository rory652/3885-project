import database as db
from hashlib import sha256
from secrets import token_hex


class Users:
    def __init__(self, password):
        self._db = db.Database("db", 6380, 0, password)

    def generate_salt(self):
        return token_hex(32)

    def add(self, username, password, permissions=0):
        # Username must be unique
        if username in self._db:
            return False

        salt = self.generate_salt()
        passHash = self.hash(password, salt)

        self._db[username] = {"hash": passHash, "salt": salt, "permissions": permissions}

        return True

    def hash(self, password, salt):
        h = sha256("".join([password, salt]).encode()).digest()

        # Repeatedly hash - slow down algorithm
        for i in range(100):
            h = sha256(h).digest()

        return sha256(h).hexdigest()

    def verify(self, username, password):
        userInfo = self._db[username]
        if userInfo is None:
            return False

        passHash = self.hash(password, userInfo["salt"])

        if passHash == userInfo["hash"]:
            return True

        return False
