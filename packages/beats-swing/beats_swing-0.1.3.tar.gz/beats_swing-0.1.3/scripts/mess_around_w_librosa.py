"""A trivial script for playing around with ideas"""

from pathlib import Path

import librosa
import librosa.display
import matplotlib.pyplot as plt


if __name__ == "__main__":
    mp3_file = (
        Path(__file__).parent.parent
        / "data"
        / "Fats Waller - Ain’t Misbehavin’ (163).mp3"
    )
    y, fs = librosa.load(str(mp3_file), sr=None)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=fs)

    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(y, sr=fs, alpha=0.6)
    plt.vlines(
        librosa.frames_to_time(beat_frames, sr=fs),
        -1,
        1,
        color="r",
        linestyle="--",
        label="Beats",
    )
    plt.title(f"Waveform with Beat Tracking; estimated tempo: {tempo}")
    plt.legend()
    plt.show()
