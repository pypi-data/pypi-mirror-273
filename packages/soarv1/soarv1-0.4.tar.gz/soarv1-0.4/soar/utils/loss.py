import inspect
import torch.nn as nn


class Loss:
    def __init__(self, config):
        loss_name = config["name"]
        loss_config = config[loss_name]
        self.loss = None
        if hasattr(nn, loss_name):
            loss = getattr(nn, loss_name)
            if isinstance(loss, type):
                sig = inspect.signature(loss.__init__)
                params = {k: v for k, v in loss_config.items() if k in sig.parameters}
                self.loss = loss(**params)

    def __call__(self):
        assert (self.loss is not None)
        return self.loss
