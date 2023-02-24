import databases.database as db


class Contacts:
    def __init__(self, password):
        self._db = db.Database("db", 6380, 2, password)

    def contains(self, contact_id):
        return contact_id in self._db

    def get(self, carehome):
        contacts = []
        for key in self._db.iterator():
            if self._db[key]["carehome"] == carehome:
                contacts.append({"contact_id": key, "who": self._db[key]["who"], "test": self._db[key]["test"], "carehome": carehome})

        return contacts

    def delete(self, contact_id):
        del self._db[contact_id]
