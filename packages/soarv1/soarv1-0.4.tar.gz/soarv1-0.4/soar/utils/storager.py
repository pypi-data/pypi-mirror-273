import os
import lmdb
from .crypt import Crypt


class Storager:
    def __init__(self, save_path, key):
        self.crypt = Crypt(key)
        self.save_path = save_path
        self.lmdbFile = lmdb.open(self.save_path, int(10 * 1024 ** 3))
        self.keys, self.lmdb_keys = self.initial()

    def __del__(self):
        self.lmdbFile.close()

    def initial(self):
        keys, lmdb_keys = [], []
        with self.lmdbFile.begin() as context:
            for key, value in context.cursor():
                lmdb_keys.append(key)
                keys.append(self.crypt.decode(key))
        return keys, lmdb_keys

    def read(self, key):
        with self.lmdbFile.begin() as context:
            buffer = None
            if key in self.keys:
                index = self.keys.index(key)
                lmdb_key = self.lmdb_keys[index]
                buffer = context.get(lmdb_key)
        return buffer

    def write(self, key, value):
        with self.lmdbFile.begin(write=True) as context:
            if key in self.keys:
                index = self.keys.index(key)
                lmdb_key = self.lmdb_keys[index]
                context.put(lmdb_key, value.getvalue())
            else:
                lmdb_key = self.crypt.encode(key)
                self.keys.append(key)
                self.lmdb_keys.append(lmdb_key)
                context.put(lmdb_key, value.getvalue())
