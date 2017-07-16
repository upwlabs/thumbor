import sys
import random
from PIL import Image
import numpy as np

remmax = lambda x: x/x.max()
remmin = lambda x: x - np.amin(x, axis=(0,1), keepdims=True)
touint8 = lambda x: (remmax(remmin(x))*(256-1e-4)).astype(int)

def arr2im(data):
    out = Image.new('RGB', data.shape[1::-1])
    out.putdata(map(tuple, data.reshape(-1, 3)))
    return out


def decode_wm(ewm):
    x, y = range(64), range(64)
    random.seed(2569)
    random.shuffle(x)
    random.shuffle(y)
    tmp = np.zeros((256, 256, 3))
    for i in range(64):
        for j in range(64):
            tmp[x[i]][y[j]] = ewm[i][j]
            tmp[64 + x[i]][y[j]] = ewm[64 + i][j]
            tmp[x[i]][64 + y[j]] = ewm[i][64 + j]
            tmp[64 + x[i]][64 + y[j]] = ewm[64 + i][64 + j]
            tmp[256 - 1 - x[i]][256 - 1 - y[j]] = ewm[256 - 1 - i][256 - 1 - j]
            tmp[256 - 64 - 1 - x[i]][256 - 1 - y[j]] = ewm[256 - 64 - 1 - i][256 - 1 - j]
            tmp[256 - 1 - x[i]][256 - 64 - 1 - y[j]] = ewm[256 - 1 - i][256 - 64 - 1 - j]
            tmp[256 - 64 - 1 - x[i]][256 - 64 - 1 - y[j]] = ewm[256 - 64 - 1 - i][256 - 64 - 1 - j]
    return tmp


def extract_wm(ori_path, wm_path):
    ori = Image.open('/Users/xinzhao/Desktop/' + ori_path)
    wm = Image.open('/Users/xinzhao/Desktop/' + wm_path)
    wm = wm.convert('RGB')
    ori_freq = np.fft.fft2(ori)
    wm_freq = np.fft.fft2(wm)
    diff = wm_freq - ori_freq
    diff = decode_wm(diff)
    diff_im = arr2im(touint8(diff))
    diff_im.save('/Users/xinzhao/Desktop/extracted_wm.jpg')
    return diff_im


if __name__ == "__main__":
    extract_wm(sys.argv[1], sys.argv[2]).show()
