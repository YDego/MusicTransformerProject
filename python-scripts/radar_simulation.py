import math
import numpy as np
from plot_manager import *
from project_variables import *


def generate_sub_function(w, epsilon, sigma):
    return [1 + math.sqrt(1 + (sigma / (max(value, 1e-3) * epsilon)) ** 2) for value in w]


def generate_alpha(w, mu=1, epsilon=1, sigma=1):
    sub_function = generate_sub_function(w, epsilon, sigma)
    alpha = [sigma * math.sqrt(mu / (2 * epsilon * max(value, 1e-3))) for value in sub_function]

    return alpha


def generate_beta(w, mu=1, epsilon=1, sigma=1):
    sub_function = generate_sub_function(w, epsilon, sigma)
    beta = [a * (math.sqrt((mu * epsilon / 2) * b)) for a, b in zip(w, sub_function)]

    return beta


def generate_amp_n_phase(alpha, beta, dist_z):
    phase = np.multiply(beta, dist_z)
    amp = np.exp(np.multiply(alpha, (-1 * dist_z)))
    return amp, phase


def create_impulse_response(amplitude, phase, df, z_dist=1, plot=True):
    # Convert amplitude and phase to complex numbers in the frequency domain
    complex_spectrum = amplitude * np.exp(np.multiply(phase, 1j))

    # Inverse Fourier Transform to obtain the time-domain signal
    impulse_response = np.fft.ifftshift(np.fft.irfft(complex_spectrum))

    # Adjust for the sampling rate
    impulse_response /= df

    # Create the time axis
    time_axis = np.linspace(0, len(impulse_response) / df, len(impulse_response), endpoint=False)

    if plot:
        plot_graph(time_axis, impulse_response, 'impulse response over time (z = {} [m])'.format(z_dist), 'time [sec]', 'amplitude []')

    return time_axis, impulse_response


if __name__ == "__main__":

    # parameters:
    epsilon = e_r * e_0
    mu = mu_r * mu_0
    sigma = 1

    # time and freq lists
    f = np.arange(0, f_end, df)
    t = np.arange(0, len(f)/df, 1/df)
    w = 2 * math.pi * f

    # amplitude constant propagation
    alpha = generate_alpha(w, mu, epsilon, sigma)
    # phase constant propagation
    beta = generate_beta(w, mu, epsilon, sigma)

    # phase and amplitude
    amp, phase = generate_amp_n_phase(alpha, beta, dist_z)
    amp = [1] * len(w)
    plot_amp_n_phase(f, amp, phase, f_start, f_end, df, dist_z)

    t_new, imp_resp = create_impulse_response(amp, phase, df, dist_z)

    # e_y = e_0 * np.multiply(amp, np.cos(wt - phase))
    # plot_graph(t, e_y)