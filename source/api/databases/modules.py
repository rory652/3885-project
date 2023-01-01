import databases.database as db
from secrets import token_hex


class Modules:
    def __init__(self, password):
        self._db = db.Database("db", 6380, 3, password)

    def get(self, module_id=None):
        if module_id is None:
            modules = []
            for key in self._db.iterator():
                # Make it cache later?
                modules.append({"module": key, "status": self._db[key]["status"]})
            return modules
        else:
            return {"module": module_id, "status": self._db[module_id]["status"]}

    def add(self, room, status='no status'):
        module_id = self.generateID()

        self._db[module_id] = {"room": room, "status": status}

        return True

    def delete(self, module_id):
        del self._db[module_id]

    def update(self, module_id, newStatus, newRoom=None):
        if newRoom is not None:
            # 'no status' = default status for new modules
            self._db[module_id] = {"room": newRoom, "status": 'no status'}

            return self._db[module_id]

        self._db[module_id] = {"room": self._db[module_id]["room"], "status": newStatus}

        return self._db[module_id]

    def generateID(self):
        new_id = token_hex(8)
        while new_id not in self._db:
            new_id = token_hex(8)

        return new_id
