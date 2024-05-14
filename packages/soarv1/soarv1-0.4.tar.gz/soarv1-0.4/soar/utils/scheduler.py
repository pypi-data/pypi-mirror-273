import inspect
from torch.optim import lr_scheduler


class Scheduler:
    def __init__(self, config, optimizer):
        scheduler_name = config["name"]
        scheduler_config = config[scheduler_name]
        self.scheduler = None
        if hasattr(lr_scheduler, scheduler_name):
            scheduler = getattr(lr_scheduler, scheduler_name)
            if isinstance(scheduler, type):
                sig = inspect.signature(scheduler.__init__)
                params = {k: v for k, v in scheduler_config.items() if k in sig.parameters}
                self.scheduler = scheduler(optimizer=optimizer, **params)

    def __call__(self):
        assert (self.scheduler is not None)
        return self.scheduler
