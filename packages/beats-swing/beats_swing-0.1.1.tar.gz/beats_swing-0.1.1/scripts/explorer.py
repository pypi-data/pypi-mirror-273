"""A little streamlit app to explore the problem space."""

from pathlib import Path

import numpy as np
import plotly.express as px
import sounddevice as sd
import streamlit as st
from pydub import AudioSegment

from beats.filtering import bass_lowpass
from beats.shared_types import Vector


if __name__ == "__main__":
    st.title("mp3 explorer")

    mp3_dir = Path(__file__).parent.parent / "data"
    mp3 = st.selectbox(
        "Which file would you like to explore?",
        options=[f for f in mp3_dir.iterdir() if f.suffix == ".mp3"],
    )

    audio = AudioSegment.from_file(str(mp3), format="mp3")
    fs = audio.frame_rate  # Sampling frequency

    samples = np.array(audio.get_array_of_samples())

    len_s = st.slider(
        "How long of a snippet would you like to analyse (in seconds)?",
        min_value=1.0,
        max_value=20.0,
        value=10.0,
    )
    starting_s = st.slider(
        "Starting point of the snippet (in seconds)",
        min_value=0.0,
        max_value=(len(samples) / fs) - len_s,
        value=20.0,
    )

    x = np.arange(starting_s, starting_s + len_s, 1 / fs)
    y = samples[int(starting_s * fs) : int((starting_s + len_s) * fs)]

    st.header("Raw signal")
    st.plotly_chart(px.line(x=x, y=y))

    # Streamlit re-runs the script from the top,
    # so we need to stop playback in-line
    sd.stop()
    if st.button("Play?", key="Play"):
        sd.play(y, fs * 2)  # No idea why we need the factor of 2 here 🙈
        if st.button("Stop?", key="Stop"):
            sd.stop()

    st.header("Spectrum")

    fft_result = np.fft.fft(y)
    n = len(fft_result)
    freq = np.fft.fftfreq(len(fft_result), 1 / fs)
    magnitude = np.abs(fft_result)
    magnitude_db = 20 * np.log10(magnitude)

    mask_low_freq = (0 < freq) & (freq < 500)

    spectrum = px.line(
        x=freq[mask_low_freq],
        y=magnitude_db[mask_low_freq],
        title="Magnitude (dB)",
    )
    st.plotly_chart(spectrum)

    st.header("Filter for bass only")

    # bass_signal = bass_band(Vector(samples), fs_d, order=5)
    gain = st.slider(
        "Amplification gain for the bass frequencies",
        min_value=0.1,
        max_value=0.5,
        value=0.25,
    )
    amplified_bass = bass_lowpass(Vector(y), fs, amplification_gain=gain)  # + samples
    # amplified_bass = samples

    # Streamlit re-runs the script from the top,
    # so we need to stop playback in-line
    sd.stop()
    if st.button("Play?", key="Bass playback"):
        sd.play(amplified_bass, fs)  # No idea why we need the factor of 2 here 🙈
        if st.button("Stop?", key="Bass stop"):
            sd.stop()

    bass_raw = px.line(
        x=x,
        y=amplified_bass,
        title="Magnitude (dB)",
    )
    st.plotly_chart(bass_raw)

    st.header("Amplified bass spectrum")
    fft_bass = np.fft.fft(amplified_bass)
    n_b = len(fft_result)
    freq_b = np.fft.fftfreq(len(fft_result), 1 / fs)
    bass_magnitude_db = 20 * np.log10(np.abs(fft_bass))

    mask_low_freq_b = (0 < freq_b) & (freq_b < 500)

    spectrum = px.line(
        x=freq_b[mask_low_freq_b],
        y=bass_magnitude_db[mask_low_freq_b],
        title="Magnitude (dB)",
    )
    st.plotly_chart(spectrum)
