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
    diff_im = arr2im(touint8(diff))
    enhance_diff(diff_im, 1.8, 2.2)
    diff_im.save('/Users/xinzhao/Desktop/extracted_wm.jpg', quality=100)
    return diff_im


if __name__ == "__main__":
    extract_wm(sys.argv[1]).show()
