import torch
import torch.nn as nn


class BotNet(nn.Module):
    def __init__(self, num_classes=1000, depth=1.0, width=1.0, weights=""):
        super(BotNet, self).__init__()

        self.in_channels = 3
        self.backbone = nn.Sequential(
            self.make_conv(Conv, out_channels=round(64 * width), repeats=1, k=3, s=2),
            self.make_conv(Conv, out_channels=round(128 * width), repeats=1, k=3, s=2),
            self.make_c2f(C2f, out_channels=round(128 * width), repeats=round(6 * depth), shortcut=True),
            self.make_conv(Conv, out_channels=round(256 * width), repeats=1, k=3, s=2),
            self.make_c2f(C2f, out_channels=round(256 * width), repeats=round(6 * depth), shortcut=True),
            self.make_conv(Conv, out_channels=round(512 * width), repeats=1, k=3, s=2),
            self.make_c2f(C2f, out_channels=round(512 * width), repeats=round(6 * depth), shortcut=True),
            self.make_conv(Conv, out_channels=round(1024 * width), repeats=1, k=3, s=2),
            self.make_c2f(C2f, out_channels=round(1024 * width), repeats=round(6 * depth), shortcut=True)
        )
        self.head = Head(self.in_channels, num_classes)

        self.init_weights(weights)

    def init_weights(self, weights):
        if len(weights):
            model = torch.load(weights)["model"]
            self.load_state_dict(model.state_dict())
        else:
            self.apply(init_weights)

    def make_conv(self, block, out_channels, repeats, k, s):
        layers = []
        for _ in range(0, repeats):
            layers.append(block(self.in_channels, out_channels, k=k, s=s))
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def make_c2f(self, block, out_channels, repeats, shortcut):
        layers = []
        for _ in range(0, repeats):
            layers.append(block(self.in_channels, out_channels, shortcut=shortcut))
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.backbone(x)
        x = self.head(x)
        return x


def init_weights(m):
    if isinstance(m, (nn.Conv2d, nn.Linear)):
        torch.nn.init.xavier_normal_(m.weight)
        if m.bias is not None:
            m.bias.data.fill_(0.01)


def auto_pad(k, p=None, d=1):  # kernel, padding, dilation
    """Pad to 'same' shape outputs."""
    if d > 1:
        k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
    if p is None:
        p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
    return p


class Conv(nn.Module):
    """Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)."""

    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
        """Initialize Conv layer with given arguments including activation."""
        super().__init__()
        default_act = [nn.ReLU(), nn.SiLU()][0]
        self.conv = nn.Conv2d(c1, c2, k, s, auto_pad(k, p, d), groups=g, dilation=d, bias=False)
        self.bn = nn.BatchNorm2d(c2)
        self.act = default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()

    def forward(self, x):
        """Apply convolution, batch normalization and activation to input tensor."""
        return self.act(self.bn(self.conv(x)))

    def forward_fuse(self, x):
        """Perform transposed convolution of 2D data."""
        return self.act(self.conv(x))


class C2f(nn.Module):
    """Faster Implementation of CSP Bottleneck with 2 convolutions."""

    def __init__(self, c1, c2, n=1, shortcut=False, g=1, e=0.5):  # ch_in, ch_out, number, shortcut, groups, expansion
        super().__init__()
        self.c = int(c2 * e)  # hidden channels
        self.cv1 = Conv(c1, 2 * self.c, 1, 1)
        self.cv2 = Conv((2 + n) * self.c, c2, 1, 1)  # optional act=FReLU(c2)
        self.m = nn.ModuleList(Bottleneck(self.c, self.c, shortcut, g, k=((3, 3), (3, 3)), e=1.0) for _ in range(n))

    def forward(self, x):
        """Forward pass through C2f layer."""
        y = list(self.cv1(x).chunk(2, 1))
        y.extend(m(y[-1]) for m in self.m)
        return self.cv2(torch.cat(y, 1))

    def forward_split(self, x):
        """Forward pass using split() instead of chunk()."""
        y = list(self.cv1(x).split((self.c, self.c), 1))
        y.extend(m(y[-1]) for m in self.m)
        return self.cv2(torch.cat(y, 1))


class Bottleneck(nn.Module):
    """Standard bottleneck."""

    def __init__(self, c1, c2, shortcut=True, g=1, k=(3, 3), e=0.5):  # ch_in, ch_out, shortcut, groups, kernels, expand
        super().__init__()
        c_ = int(c2 * e)  # hidden channels
        self.cv1 = Conv(c1, c_, k[0], 1)
        self.cv2 = Conv(c_, c2, k[1], 1, g=g)
        self.add = shortcut and c1 == c2

    def forward(self, x):
        """'forward()' applies the YOLOv5 FPN to input data."""
        return x + self.cv2(self.cv1(x)) if self.add else self.cv2(self.cv1(x))


class BottleneckCSP(nn.Module):
    """CSP Bottleneck https://github.com/WongKinYiu/CrossStagePartialNetworks."""

    def __init__(self, c1, c2, n=1, shortcut=True, g=1, e=0.5):  # ch_in, ch_out, number, shortcut, groups, expansion
        super().__init__()
        c_ = int(c2 * e)  # hidden channels
        self.cv1 = Conv(c1, c_, 1, 1)
        self.cv2 = nn.Conv2d(c1, c_, 1, 1, bias=False)
        self.cv3 = nn.Conv2d(c_, c_, 1, 1, bias=False)
        self.cv4 = Conv(2 * c_, c2, 1, 1)
        self.bn = nn.BatchNorm2d(2 * c_)  # applied to cat(cv2, cv3)
        self.act = nn.SiLU()
        self.m = nn.Sequential(*(Bottleneck(c_, c_, shortcut, g, e=1.0) for _ in range(n)))

    def forward(self, x):
        """Applies a CSP bottleneck with 3 convolutions."""
        y1 = self.cv3(self.m(self.cv1(x)))
        y2 = self.cv2(x)
        return self.cv4(self.act(self.bn(torch.cat((y1, y2), 1))))


class Head(nn.Module):
    """classification head, i.e. x(b,c1,20,20) to x(b,c2)."""

    # ch_in, ch_out, num_head, kernel, stride, padding, groups
    def __init__(self, c1, c2, k=1, s=1, p=None, g=1):
        super().__init__()
        c_ = 1280  # efficientnet_b0 size
        self.conv = Conv(c1, c_, k, s, p, g)
        self.pool = nn.AdaptiveAvgPool2d(1)  # to x(b,c_,1,1)
        self.drop = nn.Dropout(p=0.01, inplace=True)
        self.linear = nn.Linear(c_, c2)  # to x(b,c2)

    def forward(self, x):
        """Performs a forward pass of the model on input image data."""
        if isinstance(x, list):
            x = torch.cat(x, 1)
        x = self.linear(self.drop(self.pool(self.conv(x)).flatten(1)))
        return x if self.training else x.softmax(1)
