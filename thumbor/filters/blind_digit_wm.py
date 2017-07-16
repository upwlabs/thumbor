#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

import random

from PIL import Image
import numpy as np

from PIL import ImageDraw
from PIL import ImageFont


## Helper functions to rescale a frequency-image to [0, 255] and save
remmax = lambda x: x/x.max()
remmin = lambda x: x - np.amin(x, axis=(0,1), keepdims=True)
touint8 = lambda x: (remmax(remmin(x))*(256-1e-4)).astype(int)


def arr2im(data):
    out = Image.new('RGB', data.shape[1::-1])
    out.putdata(map(tuple, data.reshape(-1, 3)))
    return out

def encode_wm(wm):
    x, y = range(64), range(64)
    random.seed(2569)
    random.shuffle(x)
    random.shuffle(y)
    tmp = np.zeros((256, 256, 3))
    for i in range(64):
        for j in range(64):
            tmp[i][j] = wm[x[i]][y[j]]
            tmp[64 + i][j] = wm[x[i]][y[j]]
            tmp[i][64 + j] = wm[x[i]][y[j]]
            tmp[64 + i][64 + j] = wm[x[i]][y[j]]
            tmp[256 - 1 - i][256 - 1 - j] = wm[x[i]][y[j]]
            tmp[256 - 64 - 1 - i][256 - 1 - j] = wm[x[i]][y[j]]
            tmp[256 - 1 - i][256 - 64 - 1 - j] = wm[x[i]][y[j]]
            tmp[256 - 64 - 1 - i][256 - 64 - 1 - j] = wm[x[i]][y[j]]
    return tmp


from thumbor.filters import BaseFilter, filter_method


class Filter(BaseFilter):

    @filter_method(BaseFilter.String)
    def bdw(self, wm_str):
        engine = self.context.modules.engine
        freq = np.fft.fft2(engine.image)

        wm_im = Image.new('RGB', (64, 64), (0, 0, 0))
        draw = ImageDraw.Draw(wm_im)
        font = ImageFont.truetype("Hack-Bold.ttf", 24)
        draw.text((10, 10), wm_str[:len(wm_str) / 2], (255, 255, 255), font=font)
        draw.text((10, 34), wm_str[len(wm_str) / 2:], (255, 255, 255), font=font)
        encoded_wm = encode_wm(np.array(wm_im))
        freq_wm = freq + encoded_wm / encoded_wm.max() * 1024

        back_from_freq = np.fft.ifft2(freq_wm)
        back_from_freq = np.real(back_from_freq)
        back_from_freq_im = arr2im(back_from_freq.astype(int))

        # out = Image.new('RGB',
        #                 (bz[0] * 2, bz[1] * 2),
        #                 (0, 0, 0))
        # out.paste(im=engine.image, box=(0, 0))
        #
        # out.paste(im=back_from_freq_im, box=(bz[0], 0))
        #
        # out.paste(im=arr2im(touint8(back_from_freq - engine.image)), box=(0, bz[1]))
        #
        # freq2 = np.fft.fft2(back_from_freq_im)
        # diff = freq2 - freq
        # out.paste(im=arr2im(touint8(diff)), box=(bz[0], bz[1]))

        ori_im = Image.new('RGB', (256, 256), (0, 0, 0))
        ori_im.paste(engine.image)
        ori_im.save('/Users/xinzhao/Desktop/ori.bmp')

        engine.image = back_from_freq_im
        engine.image.format = 'PNG'

