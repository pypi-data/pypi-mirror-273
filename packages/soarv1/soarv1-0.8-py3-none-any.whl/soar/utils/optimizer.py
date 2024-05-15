import inspect
from torch import optim


class Optimizer:
    def __init__(self, config, model):
        optim_name = config["name"]
        optim_config = config[optim_name]
        self.optimizer = None
        if hasattr(optim, optim_name):
            optimizer = getattr(optim, optim_name)
            if isinstance(optimizer, type):
                sig = inspect.signature(optimizer.__init__)
                params = {k: v for k, v in optim_config.items() if k in sig.parameters}
                self.optimizer = optimizer(params=model.parameters(), **params)

    def __call__(self):
        assert (self.optimizer is not None)
        return self.optimizer
