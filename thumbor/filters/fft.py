#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

import numpy as np

from thumbor.filters.wmutils import *
from thumbor.filters import BaseFilter, filter_method


class Filter(BaseFilter):

    @filter_method(BaseFilter.String, BaseFilter.PositiveNumber)
    def fft(self, wm_str, wm_amp):
        engine = self.context.modules.engine
        base_size = engine.image.size
        bz = base_size
        engine.image = engine.image.convert('RGB')
        freq = np.fft.fft2(engine.image)

        freq_wm, ewm = wm_freq(wm_str, freq, wm_amp)

        back_from_freq = np.fft.ifft2(freq_wm)
        back_from_freq = np.real(back_from_freq)
        back_from_freq_im = arr2im(back_from_freq.astype(int))
        # back_from_freq_im = arr2im(touint8(back_from_freq))

        out = Image.new('RGB',
                        (bz[0] * 3, bz[1] * 2),
                        (0, 0, 0))
        out.paste(im=engine.image, box=(0, 0))
        out.paste(im=arr2im(touint8(freq)), box=(bz[0], 0))
        out.paste(im=arr2im(touint8(ewm)), box=(bz[0] * 2, 0))

        out.paste(im=back_from_freq_im, box=(0, bz[1]))

        # out.paste(im=arr2im(touint8(back_from_freq - engine.image)), box=(0, bz[1]))
        out.paste(im=arr2im(abs(back_from_freq - np.array(engine.image)).astype(int)), box=(bz[0], bz[1]))

        freq2 = np.fft.fft2(back_from_freq_im)
        diff = freq2 - freq
        diff = decode_wm(diff)
        # diff_im = arr2im(touint8(diff))
        diff_im = arr2im(diff.astype(int))
        enhance_diff(diff_im, 1.8, 2.2)
        out.paste(im=diff_im, box=(bz[0]*2, bz[1]))

        engine.image = out

