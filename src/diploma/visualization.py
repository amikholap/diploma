import matplotlib.pyplot as plt
import numpy as np
import scipy.misc


def time_frequency(data, size=(800, 600)):
    if np.iscomplexobj(data):
        data = np.abs(data)
    if data.shape != size:
        data = scipy.misc.imresize(data, size)
    plt.imshow(data, cmap='copper')
