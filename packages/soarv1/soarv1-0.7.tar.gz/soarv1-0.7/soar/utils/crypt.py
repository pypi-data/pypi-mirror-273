from cryptography.fernet import Fernet


class Crypt:
    def __init__(self, key):
        self.key = key
        self.crypt = Fernet(key) if len(key) else None

    def encode(self, data):
        if self.crypt is None:
            data = data.encode("utf-8")
        else:
            data = self.crypt.encrypt(data.encode("utf-8"))
        return data

    def decode(self, data):
        if self.crypt is None:
            data = data.decode("utf-8")
        else:
            data = self.crypt.decrypt(data).decode("utf-8")
        return data
