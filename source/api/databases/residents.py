import databases.database as db
from secrets import token_hex


class Residents:
    def __init__(self, password):
        self._db = db.Database("db", 6380, 1, password)

    def contains(self, resident_id):
        return resident_id in self._db

    def get(self, resident_id=None):
        if resident_id is None:
            residents = []
            for key in self._db.iterator():
                # Make it cache later?
                resident = self._db[key]
                residents.append({"resident": key, "name": resident["name"],
                                  "wearable": resident["wearable"], "covid": resident["covid"]})
            return residents
        else:
            resident = self._db[resident_id]
            return {"resident": resident_id, "name": resident["name"],
                    "wearable": resident["wearable"], "covid": resident["covid"]}

    def add(self, name, wearable, covid="false"):
        resident_id = self.generateID()

        self._db[resident_id] = {"name": name, "wearable": wearable, "covid": covid}

        return {"id": resident_id, "name": name, "wearable": wearable, "covid": covid}, 201

    def delete(self, resident_id):
        del self._db[resident_id]

    def update(self, resident_id, newName=None, newWearable=None, newStatus=None):
        if newName is None and newWearable is None and newWearable is newStatus:
            return None

        oldInfo = self._db[resident_id]

        if newName is None:
            newName = oldInfo["name"]

        if newWearable is None:
            newWearable = oldInfo["wearable"]

        if newStatus is None:
            newStatus = oldInfo["covid"]

        self._db[resident_id] = {"name": newName, "wearable": newWearable, "covid": newStatus}

        return self._db[resident_id]

    def generateID(self):
        new_id = token_hex(8)
        while new_id in self._db:
            new_id = token_hex(8)

        return new_id
