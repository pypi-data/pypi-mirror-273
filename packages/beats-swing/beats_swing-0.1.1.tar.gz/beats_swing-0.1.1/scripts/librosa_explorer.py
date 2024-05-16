"""A little streamlit app to explore the problem space."""

from pathlib import Path

import librosa
import streamlit as st
from matplotlib import pyplot as plt


if __name__ == "__main__":
    st.title("mp3 explorer")

    mp3_dir = Path(__file__).parent.parent / "data"
    mp3 = st.selectbox(
        "Which file would you like to explore?",
        options=[f for f in mp3_dir.iterdir() if f.suffix in [".mp3", ".m4a"]],
    )
    y, fs = librosa.load(str(mp3), sr=None)

    start_bpm = st.slider(
        "Initial guess at the tempo (bpm)",
        min_value=10,
        max_value=300,
        value=200,
    )
    tightness = st.slider(
        "Tightness parameter for the algo",
        min_value=10.0,
        max_value=500.0,
        value=100.0,
    )
    tempo, beat_frames = librosa.beat.beat_track(
        y=y, sr=fs, start_bpm=start_bpm, tightness=tightness
    )

    start_s, end_s = st.slider(
        "Pick the interval you'd like to visualise (time in seconds)",
        min_value=0.0,
        max_value=len(y) / fs,
        value=(30.0, 40.0),
    )
    s_idx, e_idx = int(start_s * fs), int(end_s * fs)
    y = y[s_idx:e_idx]

    fig, ax = plt.subplots()
    librosa.display.waveshow(y, sr=fs, alpha=0.6, ax=ax, offset=start_s)
    beat_times = librosa.frames_to_time(beat_frames, sr=fs)
    display_mask = (beat_times >= start_s) & (beat_times <= end_s)
    displayed_beats = beat_times[display_mask]
    ax.vlines(displayed_beats, -1, 1, color="r", linestyle="--", label="Beats")
    ax.set_title(f"Waveform with Beat Tracking; estimated tempo: {int(tempo)}bpm")
    st.pyplot(fig)
