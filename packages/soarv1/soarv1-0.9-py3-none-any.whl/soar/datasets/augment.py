import cv2
import random
import numpy as np
import albumentations as a
import torch
import torch.nn.functional as func
from torchvision import transforms


class LetterBox:
    def __init__(self, config, header):
        self.p = config["p"]
        self.fill = config["fill"]

    def __call__(self, data):
        image, label = data
        if random.random() < self.p:
            c, h, w = image.shape
            size = max(w, h)
            pad_v = (size - h) // 2
            pad_h = (size - w) // 2
            pad = (pad_h, pad_h, pad_v, pad_v)
            pad_img = func.pad(image, pad, mode='constant', value=self.fill)
        else:
            pad_img = image
        output = (pad_img, label)
        return output


class ToTensor:
    def __init__(self, config, header):
        self.transform = transforms.ToTensor()

    def __call__(self, data):
        image, label = data
        tensor = self.transform(image)
        output = (tensor, label)
        return output


class Resize:
    def __init__(self, config, header):
        width, height = config["size"]
        self.transform = transforms.Resize([height, width])

    def __call__(self, data):
        image, label = data
        resized_img = self.transform(image)
        output = (resized_img, label)
        return output


class RandomRotation:
    def __init__(self, config, header):
        p = config["p"]
        fill = config["fill"]
        degrees = config["degrees"]
        transform = transforms.RandomRotation(degrees, fill=fill)
        self.transform = transforms.RandomApply([transform], p=p)

    def __call__(self, data):
        image, label = data
        rotate_img = self.transform(image)
        output = (rotate_img, label)
        return output


class RandomHorizontalFlip:
    def __init__(self, config, header):
        self.p = config["p"]
        self.is_swap = False
        if "swap" in config.keys():
            head = config.pop("swap")
            self.swap = [header.index(h) for h in head]
            self.is_swap = len(head) == 2
            assert self.is_swap

    def __call__(self, data):
        image, label = data
        if random.random() < self.p:
            flipped_img = torch.flip(image, dims=[2])
            if self.is_swap:
                for index in self.swap:
                    label[index] = label[index] ^ 1
        else:
            flipped_img = image
        output = (flipped_img, label)
        return output


class RandomErasing:
    """
    "RandomErasing": {
          "p": 0.3,
          "scale": [
            0.02,
            0.125
          ],
          "ratio": [
            0.33,
            3.0
          ],
          "value": 0.5,
          "inplace": false
        },
    """

    def __init__(self, config, header):
        p = config["p"]
        scale = tuple(config["scale"])
        ratio = tuple(config["ratio"])
        value = config["value"]
        inplace = config["inplace"]
        self.transform = transforms.RandomErasing(p=p,
                                                  scale=scale,
                                                  ratio=ratio,
                                                  value=value,
                                                  inplace=inplace)

    def __call__(self, data):
        image, label = data
        erase_img = self.transform(image)
        output = (erase_img, label)
        return output


class RandomCrop:
    def __init__(self, config, header):
        self.p = config["p"]
        height, width = config["size"]
        fill = config["fill"]
        self.transform_crop = transforms.RandomCrop(size=[height, width], fill=fill)
        self.transform_resize = transforms.Resize([height, width])

    def __call__(self, data):
        image, label = data
        if random.random() < self.p:
            crop_img = self.transform_crop(image)
        else:
            crop_img = self.transform_resize(image)
        output = (crop_img, label)
        return output


class ColorJitter:
    def __init__(self, config, header):
        p = config["p"]
        brightness = config["brightness"]
        contrast = config["contrast"]
        saturation = config["saturation"]
        hue = config["hue"]
        transform = transforms.ColorJitter(brightness=brightness,
                                           contrast=contrast,
                                           saturation=saturation,
                                           hue=hue)
        self.transform = transforms.RandomApply([transform], p=p)

    def __call__(self, data):
        image, label = data
        color_jitter_img = self.transform(image)
        output = (color_jitter_img, label)
        return output


class Normalize:
    def __init__(self, config, header):
        self.p = config["p"]
        mean = tuple(config["mean"])
        std = tuple(config["std"])
        inplace = config["inplace"]
        self.transform = transforms.Normalize(mean=mean,
                                              std=std,
                                              inplace=inplace)

    def __call__(self, data):
        image, label = data
        if random.random() < self.p:
            normalized_img = self.transform(image)
        else:
            normalized_img = image
        output = (normalized_img, label)
        return output


class GrayScale:
    def __init__(self, config, header):
        p = config["p"]
        self.transform = transforms.RandomGrayscale(p=p)

    def __call__(self, data):
        image, label = data
        gray_img = self.transform(image)
        output = (gray_img, label)
        return output


class Blur:
    def __init__(self, config, header):
        self.p = config["p"]
        transform_list = [
            a.Blur(p=self.p),
            a.GaussianBlur(p=self.p),
            a.MedianBlur(p=self.p),
            a.CLAHE(p=self.p),
            a.RandomGamma(p=self.p),
            a.ImageCompression(p=self.p * 2,
                               quality_lower=75),
            a.RandomFog(p=self.p),
            a.RandomRain(p=self.p),
            a.RandomSnow(p=self.p),
            a.RandomShadow(p=self.p),
        ]
        self.transform = a.Compose(transform_list, p=1.0)

    def __call__(self, data):
        image, label = data
        blur_img = self.transform(image=image)['image']
        output = (blur_img, label)
        return output


class GridDropout:
    """
    "GridDropout": {
          "p": 0.99,
          "max_ratio": 0.5,
          "unit_size_min": 5,
          "unit_size_max": 30
        },
    """

    def __init__(self, config, header):
        self.p = config["p"]
        self.max_ratio = config["max_ratio"]
        self.unit_size_min = config["unit_size_min"]
        self.unit_size_max = config["unit_size_max"]

    def __call__(self, data):
        image, label = data
        ratio = self.max_ratio * random.random()
        fill_value = random.randint(0, 255)
        dropout = a.GridDropout(p=self.p, ratio=ratio,
                                random_offset=True,
                                holes_number_x=5,
                                holes_number_y=10,
                                unit_size_min=self.unit_size_min,
                                unit_size_max=self.unit_size_max,
                                fill_value=fill_value)
        dropout_img = dropout(image=image)['image']
        output = (dropout_img, label)
        return output


class GridMix:
    def __init__(self, config, header):
        self.p = config["p"]
        self.max_ratio = config["max_ratio"]
        self.min_divide = config["min_divide"]
        self.max_divide = config["max_divide"]

    def __call__(self, data):
        if random.random() < self.p:
            image, label = data
            ratio = random.uniform(0, self.max_ratio)
            x_grid_number = random.randint(self.min_divide, self.max_divide)
            y_grid_number = random.randint(self.min_divide, self.max_divide)

            height, width, _ = image.shape
            grid_width = width // x_grid_number
            grid_height = height // y_grid_number
            grid_image = image.copy()
            for _ in range(int(x_grid_number * y_grid_number * ratio)):
                row = np.random.randint(0, y_grid_number)
                col = np.random.randint(0, x_grid_number)
                start_row = row * grid_height
                end_row = start_row + grid_height
                start_col = col * grid_width
                end_col = start_col + grid_width
                if random.random() > 0.5:
                    fill = np.random.randint(0, 128, size=3)
                else:
                    fill = np.random.randint(0, 256)
                grid_image[start_row:end_row, start_col:end_col] = fill
            output = (grid_image, label)
        else:
            output = data
        return output


class AutoMix:
    def __init__(self, config, header):
        self.p = config["p"]
        self.min_ratio, self.max_ratio = config["ratio"]
        self.min_divide, self.max_divide = config["divide"]
        self.attach_image = None
        self.attach_label = None

    def __call__(self, data):
        if (random.random() < self.p
                and self.attach_image is not None
                and self.attach_label is not None):
            source_image, source_label = data
            height, width, _ = source_image.shape
            attach_image = cv2.resize(self.attach_image, (width, height))
            ratio = random.uniform(self.min_ratio, self.max_ratio)
            x_grid_number = random.randint(self.min_divide, self.max_divide)
            y_grid_number = random.randint(self.min_divide, self.max_divide)

            grid_width = width // x_grid_number
            grid_height = height // y_grid_number
            mixed_image = source_image.copy()
            for _ in range(int(x_grid_number * y_grid_number * ratio)):
                row = np.random.randint(0, y_grid_number)
                col = np.random.randint(0, x_grid_number)
                y1 = row * grid_height
                y2 = y1 + grid_height
                x1 = col * grid_width
                x2 = x1 + grid_width
                mixed_image[y1:y2, x1:x2] = attach_image[y1:y2, x1:x2]
            mixed_label = source_label * (1 - ratio) + self.attach_label * ratio
            self.attach_image, self.attach_label = data
            output = (mixed_image, mixed_label)
        else:
            self.attach_image, self.attach_label = data
            output = data
        return output


class MixUP:
    def __init__(self, config, header):
        self.p = config["p"]
        self.min_alpha, self.max_alpha = config["alpha"]
        self.attach_image = None
        self.attach_label = None

    def __call__(self, data):
        if (random.random() < self.p
                and self.attach_image is not None
                and self.attach_label is not None):
            source_image, source_label = data
            alpha = random.uniform(self.min_alpha, self.max_alpha)
            mixed_image = torch.add(torch.mul(source_image, alpha),
                                    torch.mul(self.attach_image, 1 - alpha))
            mixed_label = source_label * alpha + self.attach_label * (1 - alpha)
            self.attach_image, self.attach_label = data
            output = (mixed_image, mixed_label)
        else:
            output = data
            self.attach_image, self.attach_label = data
        return output
