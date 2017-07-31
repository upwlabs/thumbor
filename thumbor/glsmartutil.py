import numpy as np
import scipy.stats
from PIL import Image

LANCZOS = Image.LANCZOS


def pixel_entropy(im_data):
    flattened = im_data.flatten('C')
    prob = np.array([(flattened == x).sum() for x in xrange(0, 256)])
    prob = prob / float(len(flattened))
    return scipy.stats.entropy(prob)


def diff_entropy(im_data):
    diff_x = im_data[:, :1] - im_data[:, 1:]
    diff_y = im_data[:1, :] - im_data[1:, :]
    flattened_x = diff_x.flatten('C')
    flattened_y = diff_y.flatten('C')
    prob = np.array([(flattened_x == l).sum() for l in xrange(-255, 255)] +
                    [(flattened_y == l).sum() for l in xrange(-255, 255)])
    prob = prob / float(len(flattened_x) + len(flattened_y))
    return scipy.stats.entropy(prob)


def calc_im_entropy(img):
    iml = img.convert('L')
    iml_data = np.array(iml)
    px_e = pixel_entropy(iml_data)
    df_e = diff_entropy(iml_data)
    return px_e * 0.5 + df_e * 0.5


def glsmart_crop(im):
    im = im.convert('RGB')
    w, h = im.size
    if w > h:
        interval = (w - h) / 10
        sub_ims = [im.crop((interval * i, 0, h + interval * i, h)) for i in xrange(10)]
    elif h > w:
        interval = (h - w) / 10
        sub_ims = [im.crop((0, interval * i, w, w + interval * i)) for i in xrange(10)]
    else:
        return im
    scores = [calc_im_entropy(sim) for sim in sub_ims]
    print 'zx debug glsmart#scores=%r', scores
    winner_idx = scores.index(max(scores))
    return sub_ims[winner_idx]
