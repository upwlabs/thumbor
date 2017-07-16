#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from PIL import Image
import numpy as np
import scipy.fftpack as fp

from PIL import ImageDraw
from PIL import ImageFont

## Functions to go from image to frequency-image and back
im2freq = lambda data: fp.rfft(fp.rfft(data, axis=0),
                               axis=1)
freq2im = lambda f: fp.irfft(fp.irfft(f, axis=1),
                             axis=0)

## Helper functions to rescale a frequency-image to [0, 255] and save
remmax = lambda x: x/x.max()
remmin = lambda x: x - np.amin(x, axis=(0,1), keepdims=True)
touint8 = lambda x: (remmax(remmin(x))*(256-1e-4)).astype(int)

def arr2im(data):
    out = Image.new('RGB', data.shape[1::-1])
    out.putdata(map(tuple, data.reshape(-1, 3)))
    return out


from thumbor.filters import BaseFilter, filter_method


class Filter(BaseFilter):

    @filter_method()
    def fft(self):
        engine = self.context.modules.engine
        freq = np.fft.fft2(engine.image)

        # wm_im = Image.open('/Users/xinzhao/Desktop/laoshi_64.jpg')
        # wm = Image.new('RGB', (128, 128), (0, 0, 0))
        # wm.paste(wm_im, (0,0))
        # wm_im = wm_im.rotate(180)
        # wm.paste(wm_im, (64, 64, 128, 128))
        # _wm = np.array(wm)

        wm_im = Image.new('RGB', (128, 64), (0, 0, 0))
        draw = ImageDraw.Draw(wm_im)
        font = ImageFont.truetype("Hack-Regular.ttf", 32)
        for x in (0, ):
            for y in (0,  32, ):
                draw.text((x, y), "CAIJI", (255, 255, 255), font=font)
        wm = Image.new('RGB', (128, 128), (0, 0, 0))
        wm.paste(wm_im, (0, 0))
        wm_im = wm_im.rotate(180)
        wm.paste(wm_im, (0, 64))
        _wm = np.array(wm)

        freq_wm = freq + _wm / _wm.max() * 255
        # freq_wm = freq

        back_from_freq = np.fft.ifft2(freq_wm)
        back_from_freq = np.real(back_from_freq)

        base_size = engine.image.size
        bz = base_size
        out = Image.new('RGB',
                        (bz[0] * 2, bz[1] * 2),
                        (0, 0, 0))
        out.paste(im=engine.image, box=(0, 0))

        back_from_freq_im = arr2im(back_from_freq.astype(int))
        out.paste(im=back_from_freq_im, box=(bz[0], 0))

        out.paste(im=arr2im(touint8(freq_wm)), box=(0, bz[1]))

        freq2 = np.fft.fft2(back_from_freq_im)
        diff = freq2 - freq
        # out.paste(im=arr2im(diff.astype(int)), box=(bz[0], bz[1]))
        out.paste(im=arr2im(touint8(diff)), box=(bz[0], bz[1]))

        engine.image = out

