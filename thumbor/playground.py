from PIL import Image
import numpy as np
import scipy.fftpack as fp

## Functions to go from image to frequency-image and back
im2freq = lambda data: fp.rfft(fp.rfft(data, axis=0),
                               axis=1)
freq2im = lambda f: fp.irfft(fp.irfft(f, axis=1),
                             axis=0)

## Helper functions to rescale a frequency-image to [0, 255] and save
remmax = lambda x: x/x.max()
remmin = lambda x: x - np.amin(x, axis=(0,1), keepdims=True)
touint8 = lambda x: (remmax(remmin(x))*(256-1e-4)).astype(int)

def arr2im(data):
    out = Image.new('RGB', data.shape[1::-1])
    out.putdata(map(tuple, data.reshape(-1, 3)))
    return out

def watermark_on_freq(freq_data):
    data_remmin, data_min = freq_data - np.amin(freq_data, axis=(0,1), keepdims=True), \
                            np.amin(freq_data, axis=(0,1), keepdims=True)
    data_remmax, data_max = data_remmin/data_remmin.max(), data_remmin.max()

    middle_data = (data_remmax*(256-1e-4)).astype(int)
    middle_im = Image.new('RGB', middle_data.shape[1::-1])
    middle_im.putdata(map(tuple, middle_data.reshape(-1, 3)))
    wm_im = Image.new('RGB', middle_data.shape[:-1])
    wm_im.putdata(map(tuple, middle_data))
    # Stamp watermark
    wm_data = np.array(wm_im)
    wm_data = wm_data.astype(float) / (256-1e-4)
    wm_data = wm_data * data_max + data_min
    return middle_im, wm_data