#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Project      : ScreenShootResilient
# @File         : fcn_decoder.py
# @Author       : chengxin
# @Email        : zcx_language@163.com
# @Reference    : None
# @CreateTime   : 2023/11/28 14:19
#
# Import lib here
from typing import Tuple, List, Optional, Callable, Union, Any
import torch
import torch.nn as nn
from src.models.components.basic_blocks import ConvBNReLU


class FCNDecoder(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()

        self.layers = nn.Sequential(
            ConvBNReLU(in_channels, 64, 3),
            ConvBNReLU(64, 64, 3),
            ConvBNReLU(64, 64, 3)
        )
        self.conv1x1 = nn.Conv2d(64, out_channels, 1)

    def forward(self, container: torch.Tensor, normalize: bool = False):
        if normalize:
            container = (container - 0.5) * 2.
        outputs = self.layers(container)
        outputs = self.conv1x1(outputs)
        return outputs


def run():
    pass


if __name__ == '__main__':
    run()
