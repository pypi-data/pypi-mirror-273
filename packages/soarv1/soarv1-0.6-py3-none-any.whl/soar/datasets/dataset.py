import cv2
import lmdb
import numpy as np
from .transform import Transform
from torch.utils.data.dataset import Dataset
from ..utils import Crypt


class LMDBDataset(Dataset):
    def __init__(self, config, mode=None):
        self.mode = mode
        self.config = config

        self.context = None
        self.lmdb_path = config["lmdb_path"]
        self.header = self.get_header()
        self.description = self.get_description()
        self.samples = self.get_samples()
        self.transform = self.get_transform()
        self.nc = len(self.header)
        self.crypt = Crypt(self.config["key"])

    def __getitem__(self, index):
        self.init_context()
        key = self.samples[index]
        sample = self.crypt.decode(key)
        name, index, _ = eval(sample)
        label = np.zeros(self.nc, np.float64)
        label[index] = 1.0
        buffer = self.context.get(key)
        buffer = np.frombuffer(buffer, dtype=np.uint8)
        image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        image, label = self.transform(image, label)
        return image, label, name

    def __len__(self):
        return len(self.samples)

    def init_context(self):
        if self.context is None:
            self.context = self.get_context()

    def get_context(self):
        lmdb_file = lmdb.open(self.lmdb_path)
        return lmdb_file.begin()

    def get_header(self):
        context = self.get_context()
        buffer = context.get("header".encode("utf-8"))
        return eval(buffer.decode("utf-8"))

    def get_description(self):
        context = self.get_context()
        buffer = context.get("description".encode("utf-8"))
        return eval(buffer.decode("utf-8"))

    def get_samples(self):
        assert (self.mode is not None)
        context = self.get_context()
        buffer = context.get(self.mode.encode("utf-8"))
        return eval(buffer.decode("utf-8"))

    def get_transform(self):
        assert (self.mode is not None)
        config_transform = self.config["transform"][self.mode]
        return Transform(config_transform, self.header)
