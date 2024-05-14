import math
import logging
from tqdm import tqdm


class Logger:
    logging.basicConfig(level=logging.WARNING, format='%(message)s')

    def __init__(self, enable=True, space=12, scale=1e-6):
        self.enable = enable
        self.space = space
        self.scale = int(abs(math.log10(scale)))

    def __call__(self, params, pbar=None):
        if self.enable:
            if isinstance(params, list):
                description = self.merge(params)
                if isinstance(pbar, tqdm):
                    pbar.set_description(description)
                    pbar.update()
                else:
                    logging.warning(description)
            elif isinstance(params, str):
                logging.warning(params)
            else:
                logging.warning("This type of printing is not supported !")

    def merge(self, params):
        if isinstance(params, list):
            return "".join(list(map(self.format, params)))
        else:
            return params

    def format(self, param):
        if isinstance(param, float):
            return f"{f'{param:.{self.scale}f}':>{self.space}}"
        else:
            return f"{f'{param}':>{self.space}}"
