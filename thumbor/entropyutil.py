import numpy as np
import scipy.stats


def pixel_entropy(im_data):
    flattened = im_data.flatten('C')
    prob = np.array([(flattened == x).sum() for x in xrange(0, 256)])
    prob = prob / float(len(flattened))
    return scipy.stats.entropy(prob)


def diff_entropy(im_data):
    diff_x = im_data[:, :1] - im_data[:, 1:]
    diff_y = im_data[:1, :] - im_data[1:, :]
    flattened = diff_x.flatten('C') + diff_y.flatten('C')
    prob = np.array([(flattened == x).sum() for x in xrange(0, 256)])
    prob = prob / float(len(flattened))
    return scipy.stats.entropy(prob)


def calc_im_entropy(img):
    iml = img.convert('L')
    iml_data = np.array(iml)
    px_e = pixel_entropy(iml_data)
    print px_e
    df_e = diff_entropy(iml_data)
    print df_e
    return px_e * 0.5 + df_e * 0.5
