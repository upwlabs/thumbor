
import random

from PIL import Image
import numpy as np

from PIL import ImageDraw
from PIL import ImageFont


## Helper functions to rescale a frequency-image to [0, 255] and save
remmax = lambda x: x/x.max()
remmin = lambda x: x - np.amin(x, axis=(0,1), keepdims=True)
touint8 = lambda x: (remmax(remmin(x))*(256-1e-4)).astype(int)
H = 256
W = 256


def arr2im(data):
    out = Image.new('RGB', data.shape[1::-1])
    out.putdata(map(tuple, data.reshape(-1, 3)))
    return out

def wm_freq(wm_str, freq):
    wm_im = gen_wm(wm_str)
    encoded_wm = encode_wm(np.array(wm_im))
    return freq + encoded_wm / encoded_wm.max() * max((freq.max() * 0.02), W * 4)


def gen_wm(wm_str):
    wm_im = Image.new('RGB', (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(wm_im)
    font = ImageFont.truetype("Hack-Bold.ttf", 24)
    for i, j in ((1, 1), ):
        draw.text((j * 64 + 5, i * 64 + 5), wm_str[:len(wm_str) / 2], (255, 255, 255), font=font)
        draw.text((j * 64 + 5, i * 64 + 32 + 5), wm_str[len(wm_str) / 2:], (255, 255, 255), font=font)
    return wm_im

def encode_wm(wm):
    x, y = range(H/2), range(W)
    random.seed(2569)
    random.shuffle(x)
    random.shuffle(y)
    tmp = np.zeros((H, W, 3))
    for i in range(H/2):
        for j in range(W):
            tmp[i][j] = wm[x[i]][y[j]]
            tmp[H - 1 - i][W - 1 - j] = wm[x[i]][y[j]]
    return tmp


def decode_wm(ewm):
    x, y = range(H/2), range(W)
    random.seed(2569)
    random.shuffle(x)
    random.shuffle(y)
    tmp = np.zeros((H, W, 3))
    for i in range(H/2):
        for j in range(W):
            tmp[x[i]][y[j]] = ewm[i][j]
            tmp[H - 1 - x[i]][W - 1 - y[j]] = ewm[H - 1 - i][W - 1 - j]
    return tmp


