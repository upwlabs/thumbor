#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

from thumbor.filters import BaseFilter, filter_method
from thumbor.filters.wmutils import *


class Filter(BaseFilter):

    @filter_method(BaseFilter.String, BaseFilter.PositiveNumber)
    def bdw(self, wm_str, wm_amp):
        engine = self.context.modules.engine
        engine.image = engine.image.convert('RGB')
        freq = np.fft.fft2(engine.image)

        freq_wm, _ = wm_freq(wm_str, freq, wm_amp)

        back_from_freq = np.fft.ifft2(freq_wm)
        back_from_freq = np.real(back_from_freq)
        back_from_freq_im = arr2im(back_from_freq.astype(int))

        ori_im = Image.new('RGB', (W, H), (0, 0, 0))
        ori_im.paste(engine.image)
        ori_im.save('/Users/xinzhao/Desktop/ori.bmp')

        engine.image = back_from_freq_im
        engine.image.format = 'PNG'

