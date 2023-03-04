import databases.database as db
from secrets import token_hex


class Residents:
    def __init__(self, password):
        self._db = db.Database("db", 6380, 1, password)

    def contains(self, resident_id):
        return resident_id in self._db

    def get(self, carehome, resident_id=None):
        if resident_id is None:
            residents = []
            for key in self._db.iterator():
                if self._db[key]["carehome"] == carehome:
                    resident = self._db[key]
                    residents.append({"resident": key, "name": resident["name"], "carehome": resident["carehome"],
                                      "wearable": resident["wearable"], "covid": resident["covid"]})
            return residents
        else:
            if self._db[resident_id]["carehome"] == carehome:
                resident = self._db[resident_id]
                return {"resident": resident_id, "name": resident["name"],
                        "wearable": resident["wearable"], "covid": resident["covid"]}
            return "user not part of carehome", 403

    def add(self, name, wearable, carehome, covid="false"):
        resident_id = self.generateID()

        self._db[resident_id] = {"name": name, "carehome": carehome, "wearable": wearable, "covid": covid}

        return {"id": resident_id, "name": name, "carehome": carehome, "wearable": wearable, "covid": covid}, 201

    def delete(self, resident_id):
        del self._db[resident_id]

    def update(self, resident_id, carehome, newName=None, newWearable=None, newStatus=None):
        if not self._db[resident_id]["carehome"] == carehome:
            return "user not part of carehome", 403

        oldInfo = self._db[resident_id]

        if newName is None:
            newName = oldInfo["name"]

        if newWearable is None:
            newWearable = oldInfo["wearable"]

        if newStatus is None:
            newStatus = oldInfo["covid"]

        self._db[resident_id] = {"name": newName, "carehome": carehome, "wearable": newWearable, "covid": newStatus}

        return self._db[resident_id]

    def generateID(self):
        new_id = token_hex(8)
        while new_id in self._db:
            new_id = token_hex(8)

        return new_id
