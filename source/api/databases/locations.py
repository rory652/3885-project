import databases.database as db
from secrets import token_hex


class Locations:
    def __init__(self, password):
        self._db = db.Database("db", 6380, 4, password)

    def contains(self, location_id):
        return location_id in self._db

    def add(self, module, wearable, coordinates, carehome):
        location_id = self.generateID()

        self._db[location_id] = {"module": module, "wearable": wearable, "coordinates": coordinates, "carehome": carehome}

        return {"id": location_id, "data": self._db[location_id]}, 201

    def delete(self, location_id):
        del self._db[location_id]

    def generateID(self):
        new_id = token_hex(8)
        while new_id in self._db:
            new_id = token_hex(8)

        return new_id
