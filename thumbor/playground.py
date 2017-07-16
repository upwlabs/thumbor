import sys
import random
from PIL import Image
import numpy as np


from thumbor.filters.wmutils import *

def extract_wm(ori_path, wm_path):
    ori = Image.open('/Users/xinzhao/Desktop/' + ori_path)
    wm = Image.open('/Users/xinzhao/Desktop/' + wm_path)
    wm = wm.convert('RGB')
    ori_freq = np.fft.fft2(ori)
    wm_freq = np.fft.fft2(wm)
    diff = wm_freq - ori_freq
    diff = decode_wm(diff)
    diff_im = arr2im(touint8(diff))
    diff_im.save('/Users/xinzhao/Desktop/extracted_wm.jpg', quality=100)
    return diff_im


if __name__ == "__main__":
    extract_wm(sys.argv[1], sys.argv[2]).show()
