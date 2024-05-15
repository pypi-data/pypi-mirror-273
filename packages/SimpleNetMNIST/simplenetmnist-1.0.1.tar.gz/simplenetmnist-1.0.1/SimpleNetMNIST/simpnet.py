"""
An implementation of the SimpleNet slim version (310K params) and some helper
modules.
"""

import torch

from collections import OrderedDict
from torch import nn

class Scale(nn.Module):
    """
    Scales input by a scalar factor and add a scalar bias to it.

    The module is intialized as an identity operation but both the factor and
    the bias term is learnable.
    """

    def __init__(self):
        super().__init__()
        self.factor = nn.Parameter(torch.ones(1), requires_grad=True)
        self.bias = nn.Parameter(torch.zeros(1), requires_grad=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x * self.factor + self.bias

class SimpnetBlock(nn.Module):
    """
    A group of homogeneous layers used in SimpleNet.

    It contains a 3x3 convolution that can be initialized using either Xavier or
    Gaussian normal, followed by a batch normalization layer, a scaling layer,
    and a reLU layer.
    """

    def __init__(self,
                 in_channels,
                 out_channels,
                 weight_filler_type="xavier"
                 ):
        super().__init__()
        
        self.conv = nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,  # num_output
            kernel_size=3,              # kernel_size
            stride=1,                   # stride
            padding="same"              # pad
        )

        # weight_filler
        if weight_filler_type == "xavier":
            nn.init.xavier_normal_(self.conv.weight)
        elif weight_filler_type == "gaussian":
            nn.init.normal_(self.conv.weight, std=0.01)
        else:
            raise ValueError(f"invalid weight filler type {weight_filler_type}")
        
        self.bn = nn.BatchNorm2d(
            num_features=out_channels,  # num_output
            momentum=0.05,              # 1 - moving_average_fraction
            affine=False                # param
        )
        self.scale = Scale()
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.relu(self.scale(self.bn(self.conv(x))))

class SimpnetCCCP(nn.Module):
    """
    A group of layers used at the end of SimpleNet.

    It consists of a convolution layer with zero-initialized bias followed by a
    reLU layer.
    """

    def __init__(self,
                 in_channels,
                 out_channels,
                 kernel_size=1,
                 padding=0
                 ):
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            padding=padding
        )
        nn.init.constant_(self.conv.bias, 0)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.relu(self.conv(x))

class SimpnetSlim310K(nn.Module):
    """
    The slimmest SimpleNet with only 310K parameters.
    """

    def __init__(self, in_channels, out_features, ip_features=64):
        super().__init__()
        self.features = nn.Sequential(OrderedDict([
            ("block1", SimpnetBlock(in_channels=in_channels,
                                    out_channels=64)),
            ("block1_0", SimpnetBlock(in_channels=64,
                                      out_channels=32)),
            ("block2", SimpnetBlock(in_channels=32,
                                    out_channels=32,
                                    weight_filler_type="gaussian")),
            ("block2_1", SimpnetBlock(in_channels=32,
                                      out_channels=32,
                                      weight_filler_type="gaussian")),
            ("pool2_1", nn.MaxPool2d(kernel_size=2)),
            ("block2_2", SimpnetBlock(in_channels=32,
                                      out_channels=32,
                                      weight_filler_type="gaussian")),
            ("block3", SimpnetBlock(in_channels=32,
                                    out_channels=32)),
            ("conv4", nn.Conv2d(in_channels=32,
                                out_channels=64,
                                kernel_size=3,
                                stride=1,
                                padding="same")),
            ("pool4", nn.MaxPool2d(kernel_size=2)),
            ("bn4", nn.BatchNorm2d(num_features=64,
                                   momentum=0.05,
                                   affine=False)),
            ("scale4", Scale()),
            ("relu4", nn.ReLU(inplace=True)),
            ("block4_1", SimpnetBlock(in_channels=64,
                                      out_channels=64)),
            ("block4_2", SimpnetBlock(in_channels=64,
                                      out_channels=64)),
            ("pool4_2", nn.MaxPool2d(kernel_size=2)),
            ("block4_0", SimpnetBlock(in_channels=64,
                                      out_channels=128)),
            ("cccp4", SimpnetCCCP(in_channels=128,
                                  out_channels=256)),
            ("cccp5", SimpnetCCCP(in_channels=256,
                                  out_channels=64)),
            ("poolcp5", nn.MaxPool2d(kernel_size=2)),
            ("cccp6", SimpnetCCCP(in_channels=64,
                                  out_channels=64,
                                  kernel_size=3,
                                  padding=1)),
            ("poolcp6", nn.MaxPool2d(kernel_size=2)),
        ]))

        self.ip1 = nn.Linear(
            in_features=ip_features,
            out_features=out_features
        )
        nn.init.xavier_normal_(self.ip1.weight)
        nn.init.constant_(self.ip1.bias, 0)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            self.ip1
        )
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))

    def get_optimizer(self,
                      optimizer_cls: type[torch.optim.Optimizer],
                      **kwargs
                      ) -> torch.optim.Optimizer:
        """
        Creates an optimizer with learning rate and weight decay correctly
        configured for this model.

        :param optimizer_cls: the optimizer class to instantiate with
        :param kwargs: the keyword arguments to pass to the optimizer class (must contain `lr`)
        :returns: an optimizer instance correctly configured for this model
        """
        lr = kwargs["lr"]
        params = set(self.parameters())
        custom = {
            self.features.cccp4.conv.bias,
            self.features.cccp5.conv.bias,
            self.features.cccp6.conv.bias,
        }
        optimizer = optimizer_cls(
            [
                {"params": list(params - custom)},
                {"params": list(custom), "lr": 2 * lr, "weight_decay": 0}
            ],
            **kwargs
        )

        return optimizer
