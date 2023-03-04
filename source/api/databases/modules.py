import databases.database as db
from secrets import token_hex


class Modules:
    def __init__(self, password):
        self._db = db.Database("db", 6380, 3, password)

    def contains(self, module_id):
        return module_id in self._db

    def get(self, carehome, module_id=None):
        if module_id is None:
            modules = []
            for key in self._db.iterator():
                if self._db[key]["carehome"] == carehome:
                    modules.append({"module": key, "room": self._db[key]["room"], "status": self._db[key]["status"]})
            return modules
        else:
            if self._db[module_id]["carehome"] == carehome:
                return {"module": module_id, "room": self._db[module_id]["room"], "status": self._db[module_id]["status"]}
            return "user not part of carehome", 403

    def add(self, room, carehome, status='no status'):
        module_id = self.generateID()

        self._db[module_id] = {"room": room, "status": status, "carehome": carehome}

        return {"id": module_id, "data": self._db[module_id]}, 201

    def delete(self, module_id):
        del self._db[module_id]

    def update(self, module_id, carehome, newStatus, newRoom=None):
        if not self._db[module_id]["carehome"] == carehome:
            return "user not part of carehome", 403

        if newRoom is not None:
            # 'no status' = default status for new modules
            self._db[module_id] = {"room": newRoom, "status": 'no status', "carehome": carehome}

            return self._db[module_id]

        self._db[module_id] = {"room": self._db[module_id]["room"], "status": newStatus, "carehome": carehome}

        return self._db[module_id]

    def generateID(self):
        new_id = token_hex(8)
        while new_id in self._db:
            new_id = token_hex(8)

        return new_id
