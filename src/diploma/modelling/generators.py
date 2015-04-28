import numpy as np


__all__ = ['wave', 'noise', 'add']


def wave(A, f):
    @np.vectorize
    def func(t):
        return A * np.cos(2*np.pi*f*t)
    return func


def noise(ev, std):
    @np.vectorize
    def func(t):
        return np.random.normal(loc=ev, scale=std)
    return func


def add(*signals):
    @np.vectorize
    def func(t):
        return sum([s(t) for s in signals])
    return func
