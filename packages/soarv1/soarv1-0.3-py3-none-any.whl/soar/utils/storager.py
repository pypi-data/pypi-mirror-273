import os
import lmdb
from .crypt import Crypt


class Storager:
    def __init__(self, save_path, key):
        self.save_path = save_path
        self.lmdbFile = lmdb.open(self.save_path, int(10 * 1024 ** 3))
        self.crypt = Crypt(key)

    def __del__(self):
        self.lmdbFile.close()

    def read(self, key):
        with self.lmdbFile.begin() as context:
            # buffer = context.get(self.crypt.encode(key))
            buffer = self.crypt.decode(context.get(key))
        return buffer

    def write(self, key, value):
        with self.lmdbFile.begin(write=True) as context:
            # context.put(self.crypt.encode(key), value.getvalue())
            context.put(key, self.crypt.encode(value.getvalue()))
