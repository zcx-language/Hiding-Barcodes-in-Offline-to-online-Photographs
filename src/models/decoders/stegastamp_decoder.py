#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Project      : ScreenShootResilient
# @File         : stegastamp_decoder.py
# @Author       : chengxin
# @Email        : zcx_language@163.com
# @Reference    : None
# @CreateTime   : 2023/11/27 21:05
#
# Import lib here
from typing import Tuple, List, Optional, Callable, Union, Any
import torch
import torch.nn as nn
import torch.nn.functional as F
from src.models.components.basic_blocks import ConvBNReLU


class StegaStampDecoder(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()

        self.conv1 = ConvBNReLU(in_channels, 32, 3)
        self.conv2 = ConvBNReLU(32, 32, 3, stride=2)
        self.conv3 = ConvBNReLU(32, 64, 3, stride=2)
        self.conv4 = ConvBNReLU(64, 128, 3, stride=2)
        self.conv5 = ConvBNReLU(128, 256, 3, stride=2)
        self.up6 = nn.Sequential(
            nn.UpsamplingBilinear2d(scale_factor=2),
            ConvBNReLU(256, 128, 3)
        )
        self.conv6 = ConvBNReLU(256, 128, 3)
        self.up7 = nn.Sequential(
            nn.UpsamplingBilinear2d(scale_factor=2),
            ConvBNReLU(128, 64, 3)
        )
        self.conv7 = ConvBNReLU(128, 64, 3)
        self.up8 = nn.Sequential(
            nn.UpsamplingBilinear2d(scale_factor=2),
            ConvBNReLU(64, 32, 3)
        )
        self.conv8 = ConvBNReLU(64, 32, 3)
        self.up9 = nn.Sequential(
            nn.UpsamplingBilinear2d(scale_factor=2),
            ConvBNReLU(32, 32, 3)
        )
        self.conv9 = ConvBNReLU(64, 32, 3)
        self.residual = nn.Conv2d(32, out_channels, 1)

    def forward(self, image, normalize: bool = False):
        if normalize:
            image = (image - 0.5) * 2.

        conv1 = self.conv1(image)
        conv2 = self.conv2(conv1)
        conv3 = self.conv3(conv2)
        conv4 = self.conv4(conv3)
        conv5 = self.conv5(conv4)
        up6 = self.up6(conv5)
        conv6 = self.conv6(torch.cat([conv4, up6], dim=1))
        up7 = self.up7(conv6)
        conv7 = self.conv7(torch.cat([conv3, up7], dim=1))
        up8 = self.up8(conv7)
        conv8 = self.conv8(torch.cat([conv2, up8], dim=1))
        up9 = self.up9(conv8)
        conv9 = self.conv9(torch.cat([conv1, up9], dim=1))
        residual = self.residual(conv9)
        return residual


def run():
    from torchinfo import summary
    import time
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = StegaStampDecoder(3, 1).to(device)
    inputs = torch.randn(1, 3, 256, 256).to(device)
    beg_time = time.time()
    model(inputs)
    print(f"Time cost: {time.time() - beg_time}")
    pass


if __name__ == '__main__':
    run()
