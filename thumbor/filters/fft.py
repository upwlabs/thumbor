#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from thumbor.filters.wmutils import *
from thumbor.filters import BaseFilter, filter_method


class Filter(BaseFilter):

    @filter_method(BaseFilter.String)
    def fft(self, wm_str):
        engine = self.context.modules.engine
        base_size = engine.image.size
        bz = base_size
        freq = np.fft.fft2(engine.image)

        freq_wm = wm_freq(wm_str, freq)

        back_from_freq = np.fft.ifft2(freq_wm)
        back_from_freq = np.real(back_from_freq)

        out = Image.new('RGB',
                        (bz[0] * 2, bz[1] * 2),
                        (0, 0, 0))
        out.paste(im=engine.image, box=(0, 0))

        back_from_freq_im = arr2im(back_from_freq.astype(int))
        out.paste(im=back_from_freq_im, box=(bz[0], 0))

        out.paste(im=arr2im(touint8(back_from_freq - engine.image)), box=(0, bz[1]))

        freq2 = np.fft.fft2(back_from_freq_im)
        diff = freq2 - freq
        diff = decode_wm(diff)
        out.paste(im=arr2im(touint8(diff)), box=(bz[0], bz[1]))

        engine.image = out

