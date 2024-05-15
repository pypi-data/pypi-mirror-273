import torch
import torch.nn as nn


def init_weights(m):
    if isinstance(m, (nn.Conv2d, nn.Linear)):
        torch.nn.init.xavier_normal_(m.weight)
        if m.bias is not None:
            m.bias.data.fill_(0.01)


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels,
                               kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                               kernel_size=3, stride=1,
                               padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != self.expansion * out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, self.expansion * out_channels,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion * out_channels))

    def forward(self, x):
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = self.relu(out)
        return out


class ResNet18(nn.Module):
    def __init__(self, num_classes=1000, depth=1.0, width=1.0, weights=""):
        super(ResNet18, self).__init__()
        self.in_channels = round(64 * width)
        self.backbone = nn.Sequential(
            nn.Conv2d(3, round(64 * width), kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(round(64 * width)),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            self.make_layer(BasicBlock, round(64 * width), round(2 * depth), stride=1),
            self.make_layer(BasicBlock, round(128 * width), round(2 * depth), stride=2),
            self.make_layer(BasicBlock, round(256 * width), round(2 * depth), stride=2),
            self.make_layer(BasicBlock, round(512 * width), round(2 * depth), stride=2),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.head = nn.Sequential(
            nn.Linear(round(512 * width) * BasicBlock.expansion, num_classes),
            nn.Sigmoid()
        )
        self.init_weights(weights)

    def init_weights(self, weights):
        if len(weights):
            backbone = torch.load(weights)["model"].backbone
            self.backbone.load_state_dict(backbone.state_dict())
            self.head.apply(init_weights)
        else:
            self.apply(init_weights)

    def make_layer(self, block, out_channels, blocks, stride):
        layers = [block(self.in_channels, out_channels, stride)]
        self.in_channels = out_channels * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.in_channels, out_channels))
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.backbone(x)
        x = torch.flatten(x, 1)
        x = self.head(x)
        return x

