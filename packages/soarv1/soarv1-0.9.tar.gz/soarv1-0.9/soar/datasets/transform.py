from . import augment
from torchvision import transforms


class Transform:
    def __init__(self, config, header):
        augment_list = []
        for augment_name, augment_config in config.items():
            if hasattr(augment, augment_name):
                transfer = getattr(augment, augment_name)
                if isinstance(transfer, type):
                    augment_list.append(transfer(augment_config, header))
        self.transform = transforms.Compose(augment_list)

    def __call__(self, image, label):
        image, label = self.transform((image, label))
        return image, label
