"""A trivial script for playing around with ideas"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

from beats.filtering import bass_band
from beats.shared_types import Vector


if __name__ == "__main__":
    mp3_file = (
        Path(__file__).parent.parent
        / "data"
        / "Fats Waller - Ain’t Misbehavin’ (163).mp3"
    )
    audio = AudioSegment.from_file(str(mp3_file), format="mp3")
    samples = np.array(audio.get_array_of_samples())

    fft_result = np.fft.fft(samples)

    fs = audio.frame_rate  # Sampling frequency
    frequencies = np.fft.fftfreq(len(fft_result), 1 / fs)

    plt.figure(figsize=(10, 5))
    plt.plot(
        frequencies[: len(frequencies) // 2], np.abs(fft_result)[: len(fft_result) // 2]
    )  # only positive frequencies
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()

    bass_signal = bass_band(Vector(samples), fs, order=5)
    fft_bass = np.fft.fft(bass_signal)

    frequencies_bass = np.fft.fftfreq(len(fft_bass), 1 / fs)

    plt.figure(figsize=(10, 5))
    plt.plot(
        frequencies_bass[: len(frequencies_bass) // 2],
        np.abs(fft_bass)[: len(fft_bass) // 2],
    )  # only positive frequencies
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()

    # Random thoughts
    #  1. cut to only the middle of the song
