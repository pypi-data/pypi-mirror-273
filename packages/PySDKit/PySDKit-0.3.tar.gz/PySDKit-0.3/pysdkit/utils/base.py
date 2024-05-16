import numpy as np
from numpy import fft as f


class Base(object):
    """各种信号分解算法的基类"""

    @staticmethod
    def fft(ts: np.array) -> np.array:
        """Fast Fourier Transform"""
        return f.fft(ts)

    @staticmethod
    def ifft(ts: np.array) -> np.array:
        """Inverse Fast Fourier Transform"""
        return f.ifft(ts)

    @staticmethod
    def fftshift(ts: np.array) -> np.array:
        """Fast Fourier Transform Shift"""
        return f.fftshift(ts)

    @staticmethod
    def ifftshift(ts: np.array) -> np.array:
        """Inverse Fast Fourier Transform"""
        return f.ifftshift(ts)

    @staticmethod
    def fmirror(ts: np.array, sym: int) -> np.array:
        """
        Implements a signal mirroring expansion function.
        This function mirrors 'sym' elements at both the beginning and the end of the given array 'ts',
        to create a new extended array.
        :param ts: The one-dimensional numpy array to be mirrored.
        :param sym: The number of elements to mirror from both the start and the end of the array 'ts'.
                    This value must be less than or equal to half the length of the array.
        :return: The array after mirror expansion, which will have a length equal to the original
                  array length plus twice the 'sym'.
        Note:
        If 'sym' exceeds half the length of the array,
        the function may not work as expected, so it's recommended to check the value of 'sym' beforehand.
        """
        fMirr = np.append(np.flip(ts[:sym], axis=0), ts)
        fMirr = np.append(fMirr, np.flip(ts[-sym:], axis=0))
        return fMirr
