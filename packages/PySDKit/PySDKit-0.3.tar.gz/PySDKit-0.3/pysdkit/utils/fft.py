import numpy as np
from numpy import fft as f


def fft(ts: np.array) -> np.array:
    """Fast Fourier Transform"""
    return f.fft(ts)


def ifft(ts: np.array) -> np.array:
    """Inverse Fast Fourier Transform"""
    return f.ifft(ts)


def fftshift(ts: np.array) -> np.array:
    """Fast Fourier Transform Shift"""
    return f.fftshift(ts)


def ifftshift(ts: np.array) -> np.array:
    """Inverse Fast Fourier Transform"""
    return f.ifftshift(ts)
