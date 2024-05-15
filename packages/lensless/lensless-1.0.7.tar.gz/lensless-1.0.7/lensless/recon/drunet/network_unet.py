# #############################################################################
# network_unet.py
# =================
# Original Repo:
# https://github.com/cszn/DPIR/blob/15bca3fcc1f3cc51a1f99ccf027691e278c19354/models/network_unet.py
# #############################################################################

import torch
import torch.nn as nn
import lensless.recon.drunet.basicblock as B
import numpy as np

"""
# ====================
# unet
# From https://github.com/cszn/DPIR/blob/master/main_dpir_denoising.py
# ====================
"""


class UNet(nn.Module):
    def __init__(
        self,
        in_nc=1,
        out_nc=1,
        nc=[64, 128, 256, 512],
        nb=2,
        act_mode="R",
        downsample_mode="strideconv",
        upsample_mode="convtranspose",
    ):
        super(UNet, self).__init__()

        self.m_head = B.conv(in_nc, nc[0], mode="C" + act_mode[-1])

        # downsample
        if downsample_mode == "avgpool":
            downsample_block = B.downsample_avgpool
        elif downsample_mode == "maxpool":
            downsample_block = B.downsample_maxpool
        elif downsample_mode == "strideconv":
            downsample_block = B.downsample_strideconv
        else:
            raise NotImplementedError("downsample mode [{:s}] is not found".format(downsample_mode))

        self.m_down1 = B.sequential(
            *[B.conv(nc[0], nc[0], mode="C" + act_mode) for _ in range(nb)],
            downsample_block(nc[0], nc[1], mode="2" + act_mode)
        )
        self.m_down2 = B.sequential(
            *[B.conv(nc[1], nc[1], mode="C" + act_mode) for _ in range(nb)],
            downsample_block(nc[1], nc[2], mode="2" + act_mode)
        )
        self.m_down3 = B.sequential(
            *[B.conv(nc[2], nc[2], mode="C" + act_mode) for _ in range(nb)],
            downsample_block(nc[2], nc[3], mode="2" + act_mode)
        )

        self.m_body = B.sequential(
            *[B.conv(nc[3], nc[3], mode="C" + act_mode) for _ in range(nb + 1)]
        )

        # upsample
        if upsample_mode == "upconv":
            upsample_block = B.upsample_upconv
        elif upsample_mode == "pixelshuffle":
            upsample_block = B.upsample_pixelshuffle
        elif upsample_mode == "convtranspose":
            upsample_block = B.upsample_convtranspose
        else:
            raise NotImplementedError("upsample mode [{:s}] is not found".format(upsample_mode))

        self.m_up3 = B.sequential(
            upsample_block(nc[3], nc[2], mode="2" + act_mode),
            *[B.conv(nc[2], nc[2], mode="C" + act_mode) for _ in range(nb)]
        )
        self.m_up2 = B.sequential(
            upsample_block(nc[2], nc[1], mode="2" + act_mode),
            *[B.conv(nc[1], nc[1], mode="C" + act_mode) for _ in range(nb)]
        )
        self.m_up1 = B.sequential(
            upsample_block(nc[1], nc[0], mode="2" + act_mode),
            *[B.conv(nc[0], nc[0], mode="C" + act_mode) for _ in range(nb)]
        )

        self.m_tail = B.conv(nc[0], out_nc, bias=True, mode="C")

    def forward(self, x0):
        x1 = self.m_head(x0)
        x2 = self.m_down1(x1)
        x3 = self.m_down2(x2)
        x4 = self.m_down3(x3)
        x = self.m_body(x4)
        x = self.m_up3(x + x4)
        x = self.m_up2(x + x3)
        x = self.m_up1(x + x2)
        x = self.m_tail(x + x1) + x0

        return x


class UNetRes(nn.Module):
    def __init__(
        self,
        in_nc=1,
        out_nc=1,
        nc=[64, 128, 256, 512],
        nb=4,
        act_mode="R",
        downsample_mode="strideconv",
        upsample_mode="convtranspose",
    ):
        super(UNetRes, self).__init__()

        assert len(nc) == 4, "nc's length should be 4."

        self.m_head = B.conv(in_nc, nc[0], bias=False, mode="C")

        # downsample
        if downsample_mode == "avgpool":
            downsample_block = B.downsample_avgpool
        elif downsample_mode == "maxpool":
            downsample_block = B.downsample_maxpool
        elif downsample_mode == "strideconv":
            downsample_block = B.downsample_strideconv
        else:
            raise NotImplementedError("downsample mode [{:s}] is not found".format(downsample_mode))

        self.m_down1 = B.sequential(
            *[B.ResBlock(nc[0], nc[0], bias=False, mode="C" + act_mode + "C") for _ in range(nb)],
            downsample_block(nc[0], nc[1], bias=False, mode="2")
        )
        self.m_down2 = B.sequential(
            *[B.ResBlock(nc[1], nc[1], bias=False, mode="C" + act_mode + "C") for _ in range(nb)],
            downsample_block(nc[1], nc[2], bias=False, mode="2")
        )
        self.m_down3 = B.sequential(
            *[B.ResBlock(nc[2], nc[2], bias=False, mode="C" + act_mode + "C") for _ in range(nb)],
            downsample_block(nc[2], nc[3], bias=False, mode="2")
        )

        self.m_body = B.sequential(
            *[B.ResBlock(nc[3], nc[3], bias=False, mode="C" + act_mode + "C") for _ in range(nb)]
        )

        # upsample
        if upsample_mode == "upconv":
            upsample_block = B.upsample_upconv
        elif upsample_mode == "pixelshuffle":
            upsample_block = B.upsample_pixelshuffle
        elif upsample_mode == "convtranspose":
            upsample_block = B.upsample_convtranspose
        else:
            raise NotImplementedError("upsample mode [{:s}] is not found".format(upsample_mode))

        self.m_up3 = B.sequential(
            upsample_block(nc[3], nc[2], bias=False, mode="2"),
            *[B.ResBlock(nc[2], nc[2], bias=False, mode="C" + act_mode + "C") for _ in range(nb)]
        )
        self.m_up2 = B.sequential(
            upsample_block(nc[2], nc[1], bias=False, mode="2"),
            *[B.ResBlock(nc[1], nc[1], bias=False, mode="C" + act_mode + "C") for _ in range(nb)]
        )
        self.m_up1 = B.sequential(
            upsample_block(nc[1], nc[0], bias=False, mode="2"),
            *[B.ResBlock(nc[0], nc[0], bias=False, mode="C" + act_mode + "C") for _ in range(nb)]
        )

        self.m_tail = B.conv(nc[0], out_nc, bias=False, mode="C")

    def forward(self, x0):
        x1 = self.m_head(x0)
        x2 = self.m_down1(x1)
        x3 = self.m_down2(x2)
        x4 = self.m_down3(x3)
        x = self.m_body(x4)
        x = self.m_up3(x + x4)
        x = self.m_up2(x + x3)
        x = self.m_up1(x + x2)
        x = self.m_tail(x + x1)

        return x
