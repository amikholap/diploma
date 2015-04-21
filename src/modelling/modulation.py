import numpy as np
import scipy.integrate


__all__ = ['am', 'pm', 'fm']


def am(signal, carrier_amp, carrier_freq):
    def modulated(t):
        amp = carrier_amp * signal(t)
        return amp * np.cos(carrier_freq * t)
    return modulated


def pm(signal, carrier_amp, carrier_freq, m):
    def modulated(t):
        phase = carrier_freq*t + m*signal(t)
        return carrier_amp * np.cos(2 * np.pi * phase)
    return modulated


def fm(signal, carrier_amp, carrier_freq, deviation):
    def modulated(t):
        # pretty ineffective
        integral = scipy.integrate.quad(signal, 0, t)[0]
        phase = carrier_freq*t + deviation*integral
        return carrier_amp * np.cos(2 * np.pi * phase)
    return modulated
