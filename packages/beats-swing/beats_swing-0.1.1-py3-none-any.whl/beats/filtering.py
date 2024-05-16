"""This module contains filtering utilities."""

from typing import Tuple

from scipy.signal import butter
from scipy.signal import filtfilt
from scipy.signal import lfilter

from beats.shared_types import Vector


# Source: https://www.teachmeaudio.com/mixing/techniques/audio-spectrum#bass
BASS_FREQ: Tuple[float, float] = (40.0, 200.0)


def bandpass_filter(
    x: Vector, lowcut: float, highcut: float, fs: float, order: int = 5
) -> Vector:
    nyq = 0.5 * fs  # Nyquist frequency
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="band")
    y = filtfilt(b, a, x)
    return Vector(y)


def bass_band(x: Vector, fs: float, order: int = 5) -> Vector:
    lowcut, highcut = BASS_FREQ
    return bandpass_filter(x, lowcut=lowcut, highcut=highcut, fs=fs, order=order)


def bass_lowpass(
    x: Vector,
    fs: float,
    cutoff: float = BASS_FREQ[1],
    order: int = 8,
    amplification_gain: float = 1.0,
) -> Vector:
    nyq = 0.5 * fs  # Nyquist frequency
    normalized_cutoff = cutoff / nyq
    b, a = butter(order, normalized_cutoff, btype="low")

    lowpassed = lfilter(b, a, x)
    amplified_bass = lowpassed * amplification_gain

    return Vector(amplified_bass)
