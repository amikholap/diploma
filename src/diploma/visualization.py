import matplotlib.pyplot as plt
import numpy as np


def time_frequency(data):
    plt.imshow(np.abs(data), cmap='copper')
