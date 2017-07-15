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
        # engine.convert_to_grayscale()
        freq = im2freq(np.array(engine.image))
        freq_im = arr2im(touint8(freq))

        _wm = np.array(Image.open('/Users/xinzhao/Desktop/wm_laoshi.jpg'))
        freq_wm = freq + _wm

        freq_wm_im = freq2im(freq_wm)
        base_size = engine.image.size
        out = Image.new('RGB',
                        (base_size[0] * 2, base_size[1] * 2),
                        (0, 0, 0))
        out.paste(im=engine.image, box=(0, 0))
        out.paste(im=freq_im, box=(base_size[0], 0))
        out.paste(im=arr2im(touint8(wm_data)), box=(0, base_size[1]))
        out.paste(im=arr2im(touint8(back_from_freq)), box=(base_size[0], base_size[1]))

        engine.image = out

