import sys
import random
from PIL import Image
import numpy as np


from thumbor.filters.wmutils import *

def extract_wm(wm_path):
    ori = Image.open('/Users/xinzhao/Desktop/ori.bmp')
    wm = Image.open('/Users/xinzhao/Desktop/' + wm_path)
    wm = wm.convert('RGB')
    ori_freq = np.fft.fft2(ori)
    wm_freq = np.fft.fft2(wm)
    diff = wm_freq - ori_freq
    diff = decode_wm(diff)
    diff_im = arr2im(diff.astype(int))
    # enhance_diff(diff_im, 1.8, 2.2)
    res = Image.new('RGB', (ori.size[0]*2, ori.size[1]), (0, 0, 0))
    res.paste(diff_im, (0, 0))

    diff_im2 = arr2im(touint8(diff))
    res.paste(diff_im2, (ori.size[0], 0))
    res.save('/Users/xinzhao/Desktop/extracted_wm.bmp')
    return res


if __name__ == "__main__":
    extract_wm(sys.argv[1]).show()
