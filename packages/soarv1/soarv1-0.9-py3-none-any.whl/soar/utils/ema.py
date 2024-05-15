class EMA:
    def __init__(self, enable, model, decay=0.999):
        self.enable = enable
        self.model = model
        self.decay = decay
        self.shadow = {}
        self.backup = {}
        self.register()

    def register(self):
        for name, param in self.model.named_parameters():
            if param.requires_grad:
                self.shadow[name] = param.data.clone()

    def update(self):
        if self.enable:
            for name, param in self.model.named_parameters():
                if param.requires_grad:
                    assert name in self.shadow
                    average = (1.0 - self.decay) * param.data + self.decay * self.shadow[name]
                    self.shadow[name] = average.clone()

    def apply_shadow(self):
        if self.enable:
            for name, param in self.model.named_parameters():
                if param.requires_grad:
                    assert name in self.shadow
                    self.backup[name] = param.data
                    param.data = self.shadow[name]

    def restore(self):
        if self.enable:
            for name, param in self.model.named_parameters():
                if param.requires_grad:
                    assert name in self.backup
                    param.data = self.backup[name]
            self.backup = {}

