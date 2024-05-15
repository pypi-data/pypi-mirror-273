import logging
import dill as pickle
from urllib import request


class Config:
    logging.basicConfig(level=logging.WARNING, format='%(message)s')

    def __init__(self, server_url, max_number):
        self.logger = logging.getLogger()
        self.server_url = server_url
        self.max_number = max_number
        self.config = self.search()

    def search(self):
        for i in range(self.max_number):
            try:
                response = request.urlopen(self.server_url)
                return pickle.load(response)
            except Exception as e:
                self.logger.warning(f'load datasets config failed, restart...')
        self.logger.warning('try timeout, exceed the max_number, terminal!')

    def get_config(self):
        return self.config
