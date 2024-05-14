import inspect
from .. import models


class Model:
    def __init__(self, config):
        model_name = config["name"]
        model_config = config[model_name]
        self.model = None

        if hasattr(models, model_name):
            model = getattr(models, model_name)
            if isinstance(model, type):
                sig = inspect.signature(model.__init__)
                params = {k: v for k, v in model_config.items() if k in sig.parameters}
                self.model = model(**params)

    def __call__(self):
        assert (self.model is not None)
        return self.model
