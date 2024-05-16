# A series of functions for generating 1D NumPy signals
from .generator import generate_sin_signal, generate_cos_signal
from .generator import generate_square_wave, generate_triangle_wave, generate_sawtooth_wave
from .generator import generate_am_signal, generate_exponential_signal

# Generates the main test sample signal
from .generator import test_emd

# Functions that generate signal visualizations
from .generator import plot_generate_signal
