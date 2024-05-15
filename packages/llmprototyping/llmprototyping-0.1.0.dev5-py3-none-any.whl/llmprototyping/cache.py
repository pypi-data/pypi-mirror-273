import hashlib
import shelve
import pickle
import atexit

class Cache:
    def __init__(self, db_path):
        self.db = shelve.open(db_path)
        atexit.register(self.db.close)

    def __get_hash(self, key):
        return hashlib.md5(key.encode('utf8')).hexdigest()

    def purge(self, key):
        h = self.__get_hash(key)
        if h not in self.db:
            return
        items = self.db[h]
        if key in items:
            del items[key]
            self.db[h] = items
            self.db.sync()

    def put(self, key, data):
        h = self.__get_hash(key)
        if h not in self.db:
            items = {}
        else:
            items = self.db[h]

        items[key] = data
        self.db[h] = items
        self.db.sync()

    def get(self, key):
        h = self.__get_hash(key)
        if h not in self.db:
            return None

        try:
            items = self.db[h]
        except pickle.UnpicklingError:
            del self.db[h]
            self.db.sync()
        else:
            return items.get(key, None)



